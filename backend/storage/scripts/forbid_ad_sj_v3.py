# -*- coding: UTF-8 -*-
import base64
import datetime
import difflib
import hashlib
import hmac
import json
import os
import re
import socket
import struct
import sys
import time

import pypinyin
import redis
import requests

from loguru import logger
from pathlib import Path
from urllib.parse import quote_plus, urlencode

# 线上需要添加
sys.path.append('/data/crontab/')

from common.ai_platform_api import SensitiveContentDetector
from filter_api import FilterApi
from libs.basic3 import DbAct, TimeAct, RedisAct
from Xiaoshan import Xiaoshan

log_dir = Path("scripts_logs")
log_dir.mkdir(exist_ok=True)

logger.remove()
logger.add(
    sink=sys.stderr,
    level="DEBUG",
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
           "<level>{message}</level>"
)
logger.add(
    sink="scripts_logs/forbid_ad_sj_v3_{time:YYYY-MM-DD}.log",
    level="INFO",
    encoding="utf-8",
    rotation="00:00",
    retention="30 days",
    compression="zip",
    enqueue=True,
    backtrace=True,
    diagnose=False,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)


def clean_old_logs(log_dir, days=7):
    """清理旧日志文件（作为 retention 的补充）"""
    import glob
    import re
    from datetime import datetime, timedelta

    try:
        log_path = Path(log_dir)
        if not log_path.exists():
            logger.warning(f"日志目录不存在: {log_dir}")
            return

        # 查找所有匹配的日志文件（包括压缩文件）
        pattern = os.path.join(log_dir, "forbid_ad_sj_hall_*.log*")
        cutoff_date = datetime.now() - timedelta(days=days)

        removed_count = 0
        for filepath in glob.glob(pattern):
            try:
                # 从文件名中提取日期
                match = re.search(r'(\d{4}-\d{2}-\d{2})', os.path.basename(filepath))
                if match:
                    file_date = datetime.strptime(match.group(1), '%Y-%m-%d')
                    days_old = (datetime.now() - file_date).days

                    if days_old > days:
                        os.remove(filepath)
                        removed_count += 1
                        logger.info(f"✅ 删除 {days_old} 天前的日志: {os.path.basename(filepath)}")
            except Exception as e:
                logger.error(f"处理文件 {filepath} 失败: {e}")

        if removed_count > 0:
            logger.info(f"🧹 本次共清理 {removed_count} 个旧日志文件")
        else:
            logger.info(f"✓ 没有 {days} 天前的旧日志需要清理")

    except Exception as e:
        logger.error(f"清理旧日志异常: {e}")


class ForbidAdSj:
    def __init__(self):
        self.connect_db()
        self.filter_api = FilterApi()
        self.msg_type = {'1': '私聊', '2': '房间', '7': '诏令天下'}
        self.white_word = [
            '退出了语音频道',
            '开启了语音聊天',
            '/roll'
        ]
        self.api_url = 'http://10.225.138.215/v1/chat-messages'
        self.api_key = 'app-sy4mUvdx7Gg54AKbG7q2L953'
        self.detector = SensitiveContentDetector(self.api_url, self.api_key)
        self.ai_request_count = 0
        self.ai_request_delay = 1.0  # 每次请求间隔1秒
        self.ai_max_retries = 3  # 最大重试次数
        self.token = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTczMzg4OTU5MiwiZXhwIjoyMDQ5MjQ5NTkyfQ.eyJjb25maXJtIjo0NTk5Nn0.lZAnY1-ZZs0BlvWX3fz5hLL1sqDXy2Ur8xdNGcIi3FMYKF8KXDKrm2eZQA4ljpNG0gUpD5h50Zz5apR3x1dmpw'
        if os.name == 'nt':
            self.xiaoshan_url = 'https://wapi.zhimagame.net:6543/robot/webhook/v2?access_token=2027023:131839:uECMTBhApuSGSzYKjJ9PknIkb9kEdze4KSs8'  # 小邹江
        else:
            self.xiaoshan_url = 'https://wapi.zhimagame.net:6543/robot/webhook?access_token=2023949:2476:3EgpV403V5vkBn5XyFHwB7cRNVttoRRJAdw8'
        self.xs = Xiaoshan(self.xiaoshan_url)
        self.secret = 'ZV9iNUPriRNCHD0IPSZNyYhTUpXXi6AQ4ccJjaw3SnErxQ7Gyn'
        self.emoji_list = []
        for i in range(11, 61):
            self.emoji_list.append(f'#{i}')

    def connect_db(self):
        try:
            self.logs_conn = DbAct().connect_mysql("chatmsg_sj", 'utf8')
            self.logs_conn.autocommit(True)
            self.logs_cursor = self.logs_conn.cursor()

            self.db_conn = DbAct().connect_mysql("logs_sj")
            self.db_conn.autocommit(True)
            self.db_cursor = self.db_conn.cursor()

            self.main_conn = DbAct().connect_mysql("sj", 'latin1')
            self.main_conn.autocommit(True)
            self.main_cursor = self.main_conn.cursor()
            logger.success('✅ 数据库连接成功')
        except Exception as e:
            logger.error(f'❌ 数据库连接失败: {str(e)}')

    def close_db(self):
        self.logs_cursor.close()
        self.logs_conn.close()
        self.db_cursor.close()
        self.db_conn.close()

    def __del__(self):
        self.close_db()

    def hash_account(self, account):
        if not isinstance(account, bytes):
            account = bytes(account, encoding='utf8')
        account = account.lower()
        n = 0
        for x in account:
            y = x
            if y > 127:
                n = y - 256 + n
            else:
                n = y + n
        if n < 0:
            # 否则会溢出，强制类型转换为float防止溢出
            result = (n + 2 ** 32) % 10
        else:
            result = n % 10
        return result

    def detect_with_retry(self, msg, account):
        """带重试机制的AI检测"""
        if self.ai_request_count > 1:
            time.sleep(self.ai_request_delay)

        for retry in range(self.ai_max_retries):
            try:
                self.ai_request_count += 1
                result = self.detector.detect_sensitive_content(msg, account)
                if isinstance(result, dict) and "error" in result:
                    if retry < self.ai_max_retries - 1:
                        wait_time = (retry + 1) * 2
                        logger.warning(f'AI检测失败，{wait_time}秒后重试 (第{retry + 1}次): {result.get("error")}')
                        time.sleep(wait_time)
                    continue
                return result
            except Exception as e:
                if retry < self.ai_max_retries - 1:
                    wait_time = (retry + 1) * 2
                    logger.warning(f'AI检测异常，{wait_time}秒后重试 (第{retry + 1}次): {e}')
                    time.sleep(wait_time)
        logger.error(f'AI检测失败，已达最大重试次数 {self.ai_max_retries}')
        return None

    def get_abnormal_login(self, app_id):
        """
        获取高危名单里的数据，在每日落地的高危数据中，会进行单独的落地

        :param app_id: 手杀在数据部的appid
        :return: 高危账号列表
        """
        results = []
        redis_conn = RedisAct().connect_redis("xml")
        key = f'abnormal_login:{app_id}'
        all_values = redis_conn.smembers(key)
        for value in all_values:
            results.append(value)
        return results

    def parse_log(self, log):
        log_dict = {}
        temp_list = log.split(';')
        for temp in temp_list:
            try:
                key, value = temp.split(':', 1)
                log_dict[key] = value
            except:
                continue
        return log_dict['IP']

    def get_info(self, account, date):
        sql = """
            SELECT user_level, log_info 
            FROM tbl_login_%s 
            WHERE user_account='%s' 
            AND op_type IN (902, 903) 
            ORDER BY log_time DESC 
            LIMIT 1;
        """ % (date, account)
        try:
            res = self.db_cursor.execute(sql)
        except Exception:
            return (0, '')
        if res > 0:
            level, info = self.db_cursor.fetchone()
            ip = self.parse_log(info)
            return (level, ip)
        else:
            return (0, '')

    def is_forbid(self, account, date):
        sql = """
            SELECT 1 
            FROM forbit_ad 
            WHERE account='%s' 
            AND date(optime)='%s';
        """ % (account, date)
        res = self.logs_cursor.execute(sql)
        return True if res else False

    def get_idfa(self, account, ip):
        date = datetime.datetime.now().strftime('%Y%m%d')
        idfa = ''
        sql = f"""
            SELECT substring_index(substring_index(log_info, 'idfa=', -1), ';', 1) 
            FROM tbl_login_{date} 
            WHERE op_type='913' 
            AND user_account='{account}' 
            ORDER BY log_time DESC 
            LIMIT 1;
        """
        self.db_cursor.execute(sql)
        result = self.db_cursor.fetchone()
        if result is not None:
            idfa, = result
        return idfa

    def is_like_black(self, msg, blacklist, rate):
        """
        优化后的黑名单相似度判断,先清洗字符再计算相似度
        防止用符号隔开绕过检测
        """

        def clean_text(text):
            # 移除特殊符号和空格,保留中文、字母、数字
            return re.sub(r'[^\w\u4e00-\u9fff]', '', text)

        cleaned_msg = clean_text(msg)

        for item in blacklist:
            cleaned_item = clean_text(item)
            # 双重检测:原始消息和清洗后消息都计算
            sim1 = difflib.SequenceMatcher(None, msg, item).quick_ratio()
            sim2 = difflib.SequenceMatcher(None, cleaned_msg, cleaned_item).quick_ratio()
            # 取最高相似度
            if max(sim1, sim2) > rate:
                return True
        return False

    def is_like_white(self, msg, whitelist):
        for item in whitelist:
            if item in msg:
                # logger.debug(f"消息: {msg}, 包含白名单项: {item}")
                return True
        return False

    def record_to_store(self, content):
        sql = f"""
            REPLACE INTO `hws_msg`.msg_list(msg)
            VALUES ("{content}")
        """
        self.logs_cursor.execute(sql)
        logger.info(f'{content} 插入到数据库成功')

    def is_forbid_main(self, account):
        """
        只通过maychat来判断是否禁言，目前的处理封号、禁言是分开的

        :param account: 用户账号
        :return: 是否已禁言
        """
        sql = f"""
            SELECT maychat, maylogin 
            FROM tblblockaccount 
            WHERE useraccount='{account}'
        """
        self.main_cursor.execute(sql)
        result = self.main_cursor.fetchone()
        if result:
            maychat, maylogin = result
            if not isinstance(maychat, datetime.datetime) and str(maychat) != '0000-00-00 00:00:00':
                maychat = datetime.datetime.strptime(maychat, '%Y-%m-%d %X')
            if not isinstance(maylogin, datetime.datetime) and str(maylogin) != '0000-00-00 00:00:00':
                maylogin = datetime.datetime.strptime(maylogin, '%Y-%m-%d %X')
            now_time = datetime.datetime.now()
            if str(maychat) != '0000-00-00 00:00:00' and maychat > now_time:
                return True
            return False
        return False

    def get_deviceid(self, account, ip):
        date = datetime.datetime.now().strftime('%Y%m%d')
        deviceid = ''
        sql = f"""
            SELECT substring_index(substring_index(log_info, 'deviceid=', -1), ';', 1) 
            FROM tbl_login_{date} 
            WHERE op_type IN (902, 905) 
            AND log_info LIKE '%IP:{ip}%deviceid=%' 
            AND user_account='{account}' 
            ORDER BY log_time DESC 
            LIMIT 1;
        """
        self.db_cursor.execute(sql)
        result = self.db_cursor.fetchone()
        if result is not None:
            deviceid, = result
        return deviceid

    def new_forbid(self, user_account, block_time, reason, comment, why, msg_count, dest_count, msg, level, ip,
                   block_type, black=1):
        if self.is_forbid_main(user_account):
            logger.info(f'✅ 账号 {user_account} 已被封禁，跳过')
            return False

        deviceid = self.get_deviceid(user_account, ip)
        idfa = self.get_idfa(user_account, ip)

        logger.info(
            f'📌 设备信息 | 设备ID: {deviceid[:20] if deviceid else "无"}... | IDFA: {idfa[:20] if idfa else "无"}...')

        url = 'http://sjkf.ops.com/api/forbid'
        headers = {'Accept': 'application/json'}
        info = {
            "user_account": user_account,
            "block_time": block_time,
            "area_name": "area10",
            "forbid_type": block_type,
            "reason": reason,
            "comment": comment,
            "why": why,
            "token": self.token
        }

        info_json = json.dumps(info)
        res = requests.post(url, headers=headers, data=info_json)

        if res.status_code == 200:
            logger.success(f'✅ 封禁API调用成功 | 返回: {res.text}')
        else:
            logger.warning(f'⚠️ 封禁API调用异常 | 状态码: {res.status_code} | 返回: {res.text}')

        now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = f"""
            REPLACE INTO forbit_ad(account, msg_count, dest_count, msg, level, ip, optime, deviceid, idfa)
            VALUES ("{user_account}", "{msg_count}", "{dest_count}", "{msg}", "{level}", "{ip}", "{now_str}", "{deviceid}", "{idfa}")
        """
        self.logs_cursor.execute(sql)

        if black == 1:
            sql = f"REPLACE INTO blacklist_ai(msg) VALUES (\"{msg}\")"
            self.logs_cursor.execute(sql)

        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        if ip and len(ip) > 0 and ip not in ['60.190.230.178', '39.170.27.122']:
            # 查询今日该IP的封禁次数
            sql = f"SELECT count(0) FROM forbit_ad WHERE ip='{ip}' AND date(optime)='{current_date}'"
            self.logs_cursor.execute(sql)
            ip_count = 0
            for (count,) in self.logs_cursor.fetchall():
                ip_count = int(count)
                if ip_count > 20:
                    logger.warning(f'🚨 高频IP告警 | IP: {ip} | 今日已封禁: {ip_count}个账号')
                    self.xs.send_message(f'{ip} 手杀该IP多次发送广告，今日该IP已禁言{ip_count}个账号')

            # 查询该IP的总封禁次数
            sql = f"SELECT count(0) FROM forbit_ad WHERE ip='{ip}'"
            self.logs_cursor.execute(sql)
            for (count,) in self.logs_cursor.fetchall():
                ip_count = int(count)

            logger.info(f'📍 IP封禁统计 | IP: {ip} | 今日: {ip_count}次 | 总计: {ip_count}次')

            # 连接Redis并设置封禁信息
            redis_conn = redis.Redis(
                host='r-bp1ccqq4q6rnz8v2ss.redis.rds.aliyuncs.com',
                port=6379,
                password='ops:GJ82abcH'
            )

            if deviceid and len(deviceid) > 0 and str(deviceid) != '0':
                redis_conn.set(f'key:chat_forbidden:device_id:10:{deviceid}', f'{ip_count}')
                redis_conn.expire(f'key:chat_forbidden:device_id:10:{deviceid}', 604800)
                logger.info(f'📱 设备ID已记录到Redis | {deviceid[:20]}...')

            redis_conn.set(f'key:chat_forbidden:idfa:10:{idfa}', f'{ip_count}')
            redis_conn.set(f'key:chat_forbidden:ip:10:{ip}', f'{ip_count}')
            redis_conn.expire(f'key:chat_forbidden:idfa:10:{idfa}', 604800)
            redis_conn.expire(f'key:chat_forbidden:ip:10:{ip}', 604800)
            logger.info(f'🔄 Redis封禁记录已设置 | IP: {ip} | IDFA: {idfa[:20] if idfa else "无"}...')

        # 更新账号封禁次数
        if user_account not in self.count_dic:
            self.count_dic[user_account] = 0
        self.count_dic[user_account] += 1

        return True

    def cal_sign(self, params):
        '''tokens计算方法'''
        params = sorted(params.items(), key=lambda x: x[0])
        param_list = []
        for key, value in params:
            param_list.append(quote_plus(str(key)) + "=" + quote_plus(str(value)))

        string = ""
        if param_list:
            for value in param_list:
                string += value + "&"

        string = "GET" + "&" + quote_plus("/") + "&" + quote_plus(string[:-1])
        string = string.replace("%20", "\+")

        string = base64.b64encode(
            hmac.new((self.secret + '&').encode('utf-8'), string.encode('utf-8'), hashlib.sha512).digest())

        return string.decode('utf-8')

    def tell_kefu(self, account, nickname, msg, level, times, optime, notify_type, dest_count, ip, msg_type,
                  probability):
        msg_type_str = str(msg_type)
        msg_type_desc = self.msg_type.get(msg_type_str, '')
        msg_encode = msg

        sql = f"SELECT inserttime, maychat FROM tblblockaccount WHERE useraccount=\"{account}\""
        self.main_cursor.execute(sql)
        ttt = self.main_cursor.fetchone()

        if notify_type == 'warning':
            title = "多次重复警告提醒"
            sql = f"SELECT msg FROM remind WHERE msg='{msg}' AND date(optime)='{optime[0:10]}'"
            self.logs_cursor.execute(sql)
            is_remind = self.logs_cursor.fetchone()

            if is_remind is None:
                if ttt is None:
                    content = "游戏: 手杀\n账号: %s（昵称：%s，等级: %s）\n发言内容: %s（重复次数：%s）\n发言频道：%s\n提醒时间: %s\n检查结果：%s" % (
                        account, nickname, level, msg_encode, times, msg_type_desc, optime, probability)
                else:
                    inserttime, maychat = ttt
                    timenow = datetime.datetime.now().timestamp()

                    if isinstance(maychat, str):
                        if maychat == '0000-00-00 00:00:00':
                            maychat = 0
                        else:
                            maychat = datetime.datetime.strptime(maychat, '%Y-%m-%d %X')
                            maychat = maychat.timestamp()
                    else:
                        maychat = maychat.timestamp()

                    timenow = int(timenow)
                    maychat = int(maychat)

                    if maychat < timenow:
                        content = "游戏: 手杀\n账号: %s（昵称：%s，等级: %s）\n发言内容: %s（重复次数：%s）\n发言频道：%s\n提醒时间: %s\n检查结果：%s" % (
                            account, nickname, level, msg_encode, times, msg_type_desc, optime, probability)
                    else:
                        content = "游戏: 手杀\n账号: %s（昵称：%s，等级: %s）\n发言内容: %s（重复次数：%s）\n发言频道：%s\n提醒时间: %s\n检查结果：%s" % (
                            account, nickname, level, msg_encode, times, msg_type_desc, optime, probability)

                sql = f"REPLACE INTO remind(msg, optime) VALUES ('{msg}', '{optime}')"
                self.logs_cursor.execute(sql)

                if msg.find('#') > -1:
                    msg = msg.replace('#', '%23')

                url_forbid = f"http://10.225.138.125:5000/sj_forbid?user_account={account}&msg_count={times}&dest_count={dest_count}&msg={msg}&level={level}&ip={ip}"
                url_ignore = f"http://10.225.138.125:5000/sj_ignore?msg={msg}"

                content += f'[禁言]({url_forbid})\n[忽略]({url_ignore})'
                self.xs.send_markdown(content)

        elif notify_type == 'forbid':
            title = "异常言论封号提醒"
            content = "游戏: 手杀\n账号: %s（昵称：%s，等级: %s）\n发言内容: %s（重复次数：%s）\n发言频道：%s\n提醒时间: %s\n检查结果：%s" % (
                account, nickname, level, msg_encode, times, msg_type_desc, optime, probability)

            params = {'area_id': 28, 'account': account, 'optime': optime}
            sign = self.cal_sign(params)
            params['sign'] = sign

            url = f"http://118.31.246.212:3031/forbid?{urlencode(params)}"
            content += f'\n[解封]({url})'

            self.xs.send_markdown(content)

    def main(self):
        logger.info('=' * 80)
        logger.info('🚀 开始执行手杀广告检测脚本')
        logger.info('=' * 80)

        time_now = TimeAct().get_now()
        table_date = time_now[:10]
        logger.info(f'📅 当前日期: {table_date}')

        # 记录账号违规的次数
        self.count_dic = {}
        sql = f"SELECT account, count(*) FROM forbit_ad GROUP BY account"
        self.logs_cursor.execute(sql)
        for account, count in self.logs_cursor.fetchall():
            account = str(account)
            count = int(count)
            self.count_dic[account] = count
        logger.info(f'📊 历史封禁账号数: {len(self.count_dic)}')

        # 封禁的账号
        forbid_account = set()
        sql = f"SELECT account FROM forbit_ad WHERE date(optime)='{table_date}'"
        self.logs_cursor.execute(sql)
        for account, in self.logs_cursor.fetchall():
            account = str(account)
            forbid_account.add(account)
        logger.info(f'📋 今日已封禁账号数: {len(forbid_account)}')

        # 查询聊天信息
        table_date_formatted = table_date.replace('-', '')
        sql = f"""
            SELECT account, nk, count(0), count(DISTINCT dest_nk), msg, LENGTH(msg), min(id), max(id), msg_type
            FROM `chatmsg_%s`
            WHERE msg_type IN (1, 2)
            AND length(msg) > 5
            AND optime > DATE_SUB(NOW(), INTERVAL 10 MINUTE)
            GROUP BY account, msg
            HAVING count(*) >= 5;
        """ % table_date_formatted

        logger.info(f'🔍 查询SQL: {sql}')
        self.logs_cursor.execute(sql)
        info = self.logs_cursor.fetchall()
        logger.info(f'📊 查询到 {len(info)} 条待检测数据')

        # 加载黑名单和白名单
        blacklist = []
        whitelist = []

        self.logs_cursor.execute("SELECT msg FROM blacklist_ai")
        for (msg,) in self.logs_cursor.fetchall():
            blacklist.append(msg)
        logger.info(f'🔴 黑名单样本数: {len(blacklist)}')

        self.logs_cursor.execute("SELECT msg FROM whitelist")
        for (msg,) in self.logs_cursor.fetchall():
            whitelist.append(msg)
        logger.info(f'⚪ 白名单样本数: {len(whitelist)}')

        # 高风险账号
        abnormal_login = self.get_abnormal_login('205_694')
        logger.warning(f'⚠️ 高风险账号有 {len(abnormal_login)} 个')

        if len(info) > 0:
            logger.info('🔄 开始处理数据...')
            logger.info('-' * 80)

            process_count = 0  # 处理计数
            forbid_count = 0  # 封禁计数
            skip_count = 0  # 跳过计数

            for (account, nickname, count, dest_count, msg, msg_len, min_id, max_id, msg_type) in info:
                process_count += 1
                msg_type_str = str(msg_type)
                msg_encode = msg

                logger.info(f'\n📌 [{process_count}/{len(info)}] 处理账号: {account} | 昵称: {nickname}')

                # 今日已封禁的账号直接跳过
                if account in forbid_account:
                    logger.info(f'✅ 账号 {account} 今日已处理，跳过')
                    skip_count += 1
                    continue

                # 过滤表情包
                emoji_count = 0
                emoji_filtered = []
                for i in self.emoji_list:
                    if i in msg_encode:
                        msg_encode = msg_encode.replace(i, '')
                        emoji_filtered.append(i)
                        emoji_count += 1
                if emoji_count > 0:
                    logger.info(f'😊 过滤表情包: {emoji_count}个 | 表情: {emoji_filtered}')

                # 获取玩家账号等级和IP
                level, ip = self.get_info(account, table_date_formatted)
                nickname_encode = nickname

                # 白名单检查
                if msg_encode in self.white_word:
                    logger.info(f'✅ 白名单台词 | 内容: {msg_encode}...')
                    skip_count += 1
                    continue

                # 检查过滤后消息长度,过短则跳过
                if len(msg_encode.strip()) <= 2:
                    logger.info(f'✅ 过滤后消息过短 | 原始: {msg} | 过滤后: {msg_encode}')
                    skip_count += 1
                    continue

                # 未处理的输出信息观察
                logger.info(
                    f"📊 发言次数: {count} | 目标数: {dest_count} | 等级: {level} | 长度: {msg_len} | 内容: {msg_encode} | 频道: {self.msg_type[msg_type_str]} | 📍 IP: {ip}"
                )

                if self.is_like_white(msg, self.white_word):
                    logger.info(f'✅ 相似白名单内容，跳过检测: {msg}...')
                    skip_count += 1
                    continue

                # 各环节打标使用
                forbid_flag = False
                category = ''

                if self.is_like_black(msg, blacklist, 0.8):
                    logger.warning(f'🔴 黑名单命中 | 账号: {account} | 内容: {msg}')
                    category = '已存在黑名单样本中'
                    forbid_flag = True
                elif count >= 50:
                    logger.warning(f'🔴 重复次数过多 | 账号: {account} | 次数: {count} | 内容: {msg}')
                    category = '重复言论次数过多'
                    forbid_flag = True
                else:
                    # 黄位森接口，判断是否为广告
                    filter_data = self.filter_api.is_ad_content_v2(msg)
                    if filter_data:
                        prediction = filter_data['prediction']
                        category = filter_data['category']
                        confidence = filter_data['confidence']

                        logger.info(
                            f'🤖 广告检测结果 | 内容: {msg} | prediction={prediction} | category={category} | confidence={confidence:.2%}')

                        if prediction == 1 and confidence > 0.9:
                            logger.warning(
                                f'🟠 广告接口命中 | 内容: {msg} | 账号: {account} | 内容: {msg} | 概率: {confidence:.2%}')
                            forbid_flag = True
                        elif prediction == 1:
                            # 预过滤系统提示类消息
                            if any(keyword in msg for keyword in self.white_word):
                                logger.info(f'✅ 白名单内容，跳过AI检测: {msg}...')
                                skip_count += 1
                                continue

                            logger.info(
                                f'🟡 广告概率较低 | 内容: {msg} | 账号: {account} | 概率: {confidence:.2%} | 启动CHAN AI检测')

                            if account in abnormal_login:
                                logger.warning(f'⚠️ 高风险账号检测 | 内容: {msg} | 账号: {account}')
                                category = '高风险账号'
                                forbid_flag = True

                            result = self.detect_with_retry(msg, account)
                            logger.warning(f'🤖 AI检测结果: {result}')

                            # 从返回结果中提取相关字段
                            is_sensitive = result.get('is_sensitive', False)
                            reason = result.get("reason", "无原因说明")
                            risk_level = result.get("risk_level", "无风险等级")  # 封禁的话只取high等级的
                            risk_probability = result.get("risk_probability", "0.0000")  # 风险概率
                            detected_words = result.get("detected_words", [])

                            if is_sensitive and risk_level == 'high':
                                # 记录未做判断的语句，用作语料
                                self.record_to_store(msg)
                                logger.success(
                                    f'🔴 AI检测命中 | 内容: {msg} | 账号: {account} | 风险: {risk_level} | 原因: {reason} | 敏感词: {detected_words}')
                                forbid_flag = True
                            else:
                                logger.info(
                                    f'✅ AI检测通过 | 内容: {msg} | 账号: {account} | 风险: {risk_level} | 概率: {risk_probability} | 原因: {reason} | 敏感词: {detected_words}')
                    else:
                        logger.warning(f'⚠️ 广告检测接口返回异常 | 账号: {account}')

                if forbid_flag:
                    forbid_count += 1
                    block_time = 7
                    block_type = 'chat'
                    forbid_count_history = self.count_dic.get(account, 0)

                    if forbid_count_history > 3:
                        block_time = 30
                        block_type = 'chat'
                    if forbid_count_history > 5:
                        block_time = 365
                        block_type = 'chat'

                    logger.info(f'📌 历史封禁: {forbid_count_history}次 | 本次封禁: {block_time}天')

                    forbid_result = self.new_forbid(
                        account, block_time, '多次发布广告信息或异常言论',
                        f'{category}，如有疑问联系陈旭', '0', count,
                        dest_count, msg, level, ip, block_type
                    )

                    if forbid_result:
                        logger.success(f'✅ 封禁完成 | 账号: {account} | 时长: {block_time}天')
                        self.tell_kefu(
                            account, nickname_encode, msg, level, count, time_now, 'forbid',
                            dest_count, ip, msg_type, category
                        )
                    else:
                        logger.error(f'⚠️ 封禁失败 | 账号: {account}')

            logger.info('-' * 80)
            logger.info(
                f'📊 处理完成 | 总数: {len(info)} | 处理: {process_count} | 封禁: {forbid_count} | 跳过: {skip_count}')

        logger.info('=' * 80)
        logger.info('✅ 脚本执行完成')
        logger.info('=' * 80)


if __name__ == '__main__':
    script_name = os.path.basename(__file__)

    if os.name == 'nt':
        # Windows系统直接执行
        pass
    else:
        # Linux系统检查是否已在运行
        cmd = f'ps aux | grep {script_name} | grep -v grep'
        result = os.popen(cmd).readlines()

        if len(result) > 1:
            logger.warning(f'⚠️ 脚本 {script_name} 已在运行，退出...')
            sys.exit(0)

    # 查询当前10分钟内的数据，脚本执行频率为10分钟
    # 清理旧日志
    clean_old_logs("scripts_logs", days=5)

    ForbidAdSj().main()

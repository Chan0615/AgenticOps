import requests
import json
import time
from typing import Dict, Any, Optional


class SensitiveContentDetector:
    def __init__(self, api_url: str, api_key: str, max_retries: int = 3, retry_delay: float = 2.0):
        self.api_url = api_url
        self.headers = {
            'Content-Type': "application/json",
            'Authorization': f'Bearer {api_key}'
        }
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def get_detection_prompt(self) -> str:
        return """
你是一名专业的中文内容安全审核专家。请对以下文本进行严格的多维度违规检测。

## 【检测维度与判定标准】

### 1. 政治敏感（高风险）
**判定标准：**
- 涉及国家领导人姓名、职务、代称
- 涉及敏感政治事件、历史事件
- 涉及敏感政治词汇（如颠覆、反动等）
- 涉及港澳台敏感表述
- 涉及境外政治组织

**变体形式：** 拼音缩写、谐音、符号分隔、数字替代

---

### 2. 色情低俗（高风险）
**判定标准：**
- 直接性描述、性暗示词汇
- 招嫖、约炮、色情服务
- 色情资源传播
- 性器官名称或代称
- 暧昧、挑逗性语言

**变体形式：**
- 拼音缩写：yue、cp、ghs
- 数字谐音：4h、②②
- 符号替代
- 英文混用：make love、ONS

---

### 3. 诈骗欺诈（高风险）
**判定标准：**
- 账号交易（卖号、买号、代练、租号）
- 虚假兼职（刷单、点赞赚钱）
- 金融诈骗（贷款、投资、高收益）
- 中奖诈骗
- 冒充官方客服

**变体形式：**
- Q代替群、V代替微信
- 数字分隔联系方式
- 谐音：兼zhi、刷dan

---

### 4. 广告营销（中高风险）
**判定标准：**
- 游戏代练、代打、陪玩
- 账号买卖、装备交易
- 外挂、脚本、辅助工具
- 第三方充值
- 引流到其他平台

---

### 5. 违禁品违法（高风险）
**判定标准：**
- 毒品及代称
- 赌博相关
- 管制物品

---

### 6. 暴恐极端（高风险）
**判定标准：**
- 暴力、恐怖内容
- 极端主义言论
- 仇恨言论

---

### 7. 脏话攻击（中风险）
**判定标准：**
- 脏话、粗口
- 人身攻击、侮辱性语言
- 歧视性言论

---

## 【变体识别规则】

以下情况必须标记为违规：
1. 拼音缩写
2. 谐音替代
3. 符号分隔
4. 数字替代
5. 英文混用
6. 上下文暗示

---

## 【输出格式】

必须以JSON格式返回，不要包含任何其他内容：

{
    "is_sensitive": true/false,
    "risk_level": "high/medium/low",
    "risk_probability": 0.95,
    "categories": ["色情", "诈骗"],
    "reason": "详细说明违规原因",
    "suggestion": "处理建议",
    "detected_words": ["违规词1"],
    "confidence": "certain/likely/uncertain"
}

字段说明：
- is_sensitive: 是否有违规内容
- risk_level: high/medium/low
- risk_probability: 违规概率 0-1
- categories: 违规类别数组
- reason: 判定理由
- suggestion: 处理建议
- detected_words: 检测到的违规词
- confidence: 置信度

---

## 【重要原则】

1. 宁可误判，不可漏判
2. 上下文分析
3. 变体敏感
4. 严格标准
"""

    def detect_sensitive_content(self, input_text: str, user_id: str = "default_user") -> Dict[Any, Any]:
        """检测敏感内容"""
        # 将检测提示作为系统提示与输入文本结合
        detection_prompt = self.get_detection_prompt()
        full_prompt = f"{detection_prompt}\n\n需要检测的文本内容：\n{input_text}"

        payload = {
            "inputs": {},
            "query": full_prompt,
            "response_mode": "blocking",
            "user": user_id
        }
        
        # 打印请求体以便调试
        print(f"[调试] 请求payload大小: {len(json.dumps(payload, ensure_ascii=False))} 字符")

        try:
            # 使用带重试机制的请求方法
            response = self.call_api_with_retry(payload, timeout=30)
            
            if response is None:
                return {"error": f"请求失败，已重试 {self.max_retries} 次后放弃"}
            
            result = response.json()

            # 打印原始响应以便调试
            print("\n" + "*" * 30 + "API 原始响应" + "*" * 30 + "\n")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            print("*" * 60 + "\n")

            # 如果返回的是事件格式，提取实际答案
            if "answer" in result and result.get("event") == "message":
                try:
                    answer_content = result["answer"]
                    # 去除可能的 Markdown 代码块标记
                    if answer_content.strip().startswith("```json"):
                        answer_content = answer_content.strip().replace("```json", "").replace("```", "")
                    elif answer_content.strip().startswith("```"):
                        answer_content = answer_content.strip().replace("```", "")
                    # 去除可能的前后空白字符
                    answer_content = answer_content.strip()
                    answer_json = json.loads(answer_content)
                    # 添加完整的API响应信息
                    answer_json["conversation_id"] = result.get("conversation_id", "")
                    answer_json["user"] = user_id
                    return answer_json
                except json.JSONDecodeError as e:
                    print(f"[警告] 无法解析 answer 字段: {e}")
                    print(f"[原始 answer 内容]: {result.get('answer', '')[:200]}...")
                    return {
                        "raw_answer": result["answer"],
                        "full_response": result,
                        "parse_error": str(e)
                    }
            else:
                print("[警告] 响应格式不符合预期，未找到 answer 字段")
                return result

        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return {"error": f"响应不是有效的JSON: {e}"}

    def call_api_with_retry(self, payload: Dict[str, Any], timeout: int = 30) -> Optional[requests.Response]:
        """
        带重试机制的AI请求方法
        
        Args:
            payload: 请求体
            timeout: 单次请求超时时间（秒）
            
        Returns:
            requests.Response: 成功时返回响应对象，失败时返回None
        """
        last_exception = None
        
        for attempt in range(1, self.max_retries + 1):
            try:
                print(f"[重试机制] 第 {attempt}/{self.max_retries} 次尝试请求...")
                
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=timeout
                )
                response.raise_for_status()
                
                print(f"[重试机制] 第 {attempt} 次请求成功")
                return response
                
            except requests.exceptions.Timeout as e:
                last_exception = e
                print(f"[重试机制] 第 {attempt} 次请求超时: {e}")
                
            except requests.exceptions.ConnectionError as e:
                last_exception = e
                print(f"[重试机制] 第 {attempt} 次连接错误: {e}")
                
            except requests.exceptions.HTTPError as e:
                # 打印详细的错误响应内容以便调试
                if e.response is not None:
                    try:
                        error_detail = e.response.json()
                        print(f"[重试机制] HTTP错误详情: {json.dumps(error_detail, ensure_ascii=False)}")
                    except:
                        print(f"[重试机制] HTTP错误响应: {e.response.text[:500]}")
                
                # HTTP错误（如5xx）通常可以重试
                if e.response.status_code >= 500:
                    last_exception = e
                    print(f"[重试机制] 第 {attempt} 次服务器错误 (HTTP {e.response.status_code}): {e}")
                else:
                    # 4xx错误通常是客户端错误，不需要重试
                    print(f"[重试机制] HTTP客户端错误 (HTTP {e.response.status_code})，停止重试: {e}")
                    return None
                    
            except requests.exceptions.RequestException as e:
                last_exception = e
                print(f"[重试机制] 第 {attempt} 次请求异常: {e}")
            
            # 如果不是最后一次尝试，则等待后重试
            if attempt < self.max_retries:
                wait_time = self.retry_delay * attempt  # 指数退避
                print(f"[重试机制] 等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
        
        print(f"[重试机制] 所有 {self.max_retries} 次尝试均失败，最后错误: {last_exception}")
        return None


def main():
    api_url = 'http://10.225.138.215/v1/chat-messages'
    api_key = 'app-RWxtq1TtjglWd4KGbVXbA4zb'  # 和谐社会的key 模型：qwen3.5-plus-2026-02-15(Qwen3.5)

    detector = SensitiveContentDetector(api_url, api_key)

    # 测试文本
    test_text = "青江革文好命"
    # test_text = "是Q是群，962685753加我，有美女图片"
    # test_text = "有没有# 有时间？帮我托到年 酬  一千八 家我"
    result = detector.detect_sensitive_content(test_text, "whoami")

    # 最终结果处理
    print("\n" + "=" * 30 + "最终处理结果" + "=" * 30)
    # 从返回结果中提取 is_sensitive
    is_sensitive = result.get("is_sensitive", False)

    if "error" in result:
        print(f"[错误] {result.get('error')}")
    elif is_sensitive:
        risk_level = result.get("risk_level", "无风险等级")
        risk_probability = float(result.get("risk_probability", 0.0000))
        reason = result.get("reason", "无原因说明")
        suggestion = result.get("suggestion", "")
        detected_words = result.get("detected_words", [])

        print(f"[✓] 内容包含敏感信息")
        print(f"[会话ID-conversation_id] {result.get('conversation_id', '')}")
        print(f"[用户ID-user] {result.get('user', '')}")
        print(f"[风险等级-risk_level] {risk_level}")
        print(f"[风险概率-risk_probability] {risk_probability:.4f}")
        print(f"[原因-reason] {reason}")
        if suggestion:
            print(f"[建议-suggestion] {suggestion}")
        if detected_words:
            print(f"[敏感词-detected_words] {', '.join(detected_words)}")
    else:
        print(f"[✓] 内容安全，未检测到敏感信息")
    print("=" * 60)


if __name__ == "__main__":
    main()

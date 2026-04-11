"""Cron helper utilities for validation, description and preview."""

import re
from datetime import datetime

from cron_descriptor import Options, get_description
from croniter import croniter


_WEEKDAY_MAP = {
    "一": "1",
    "二": "2",
    "三": "3",
    "四": "4",
    "五": "5",
    "六": "6",
    "日": "0",
    "天": "0",
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "0",
}


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", "", text or "")


def _parse_hhmm(text: str) -> tuple[int, int]:
    match = re.search(r"(?P<hour>\d{1,2})[:：](?P<minute>\d{1,2})", text)
    if not match:
        raise ValueError("请包含时间，例如 18:30")

    hour = int(match.group("hour"))
    minute = int(match.group("minute"))
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        raise ValueError("时间格式不合法，请使用 00:00 - 23:59")
    return hour, minute


def describe_cron_zh(cron_expression: str) -> str:
    options = Options()
    options.locale_code = "zh_CN"
    return get_description(cron_expression, options)


def validate_cron(cron_expression: str) -> tuple[bool, str | None]:
    expr = (cron_expression or "").strip()
    if not expr:
        return False, "Cron表达式不能为空"
    try:
        croniter(expr, datetime.now())
        return True, None
    except Exception as exc:
        return False, str(exc)


def preview_next_runs(cron_expression: str, count: int = 7, start_time: datetime | None = None) -> list[datetime]:
    base_time = start_time or datetime.now()
    iterator = croniter(cron_expression, base_time)
    return [iterator.get_next(datetime) for _ in range(count)]


def natural_to_cron(text: str) -> str:
    raw = _normalize_text(text)
    if not raw:
        raise ValueError("自然语言描述不能为空")

    every_minute_match = re.fullmatch(r"每(\d{1,2})分钟", raw)
    if every_minute_match:
        step = int(every_minute_match.group(1))
        if step < 1 or step > 59:
            raise ValueError("分钟步长需在 1-59")
        return f"*/{step} * * * *"

    every_hour_match = re.fullmatch(r"每(\d{1,2})小时", raw)
    if every_hour_match:
        step = int(every_hour_match.group(1))
        if step < 1 or step > 23:
            raise ValueError("小时步长需在 1-23")
        return f"0 */{step} * * *"

    if raw in {"每小时", "每小时执行"}:
        return "0 * * * *"

    if raw.startswith("每天"):
        hour, minute = _parse_hhmm(raw)
        return f"{minute} {hour} * * *"

    if raw.startswith("工作日") or raw.startswith("每个工作日") or raw.startswith("每周一到周五"):
        hour, minute = _parse_hhmm(raw)
        return f"{minute} {hour} * * 1-5"

    week_match = re.fullmatch(r"每周([一二三四五六日天0-7,，、]+)(\d{1,2}[:：]\d{1,2})", raw)
    if week_match:
        week_raw = week_match.group(1)
        hour, minute = _parse_hhmm(week_match.group(2))
        normalized_week = week_raw.replace("，", ",").replace("、", ",")
        values = []
        for token in normalized_week.split(","):
            token = token.strip()
            if not token:
                continue
            mapped = _WEEKDAY_MAP.get(token)
            if mapped is None:
                raise ValueError(f"无法识别星期: {token}")
            values.append(mapped)
        if not values:
            raise ValueError("请提供星期信息")
        dow = ",".join(dict.fromkeys(values))
        return f"{minute} {hour} * * {dow}"

    month_match = re.fullmatch(r"每月([0-9,，、]+)号?(\d{1,2}[:：]\d{1,2})", raw)
    if month_match:
        days_raw = month_match.group(1).replace("，", ",").replace("、", ",")
        hour, minute = _parse_hhmm(month_match.group(2))
        days = []
        for token in days_raw.split(","):
            token = token.strip()
            if not token:
                continue
            day = int(token)
            if day < 1 or day > 31:
                raise ValueError("每月日期需在 1-31")
            days.append(str(day))
        if not days:
            raise ValueError("请提供每月执行日期")
        dom = ",".join(dict.fromkeys(days))
        return f"{minute} {hour} {dom} * *"

    raise ValueError(
        "无法识别自然语言，请使用例如：每天18:30、工作日09:00、每周一,三,五20:00、每月5,25,28号18:30"
    )

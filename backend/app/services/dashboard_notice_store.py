"""Dashboard notice file store."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from threading import Lock
import json


_STORE_LOCK = Lock()
_STORE_PATH = Path(__file__).resolve().parents[2] / "data" / "dashboard_notices.json"


def _ensure_store() -> None:
    _STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not _STORE_PATH.exists():
        _STORE_PATH.write_text("[]", encoding="utf-8")


def _read_notices() -> list[dict]:
    _ensure_store()
    with _STORE_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
        return data if isinstance(data, list) else []


def _write_notices(notices: list[dict]) -> None:
    _ensure_store()
    with _STORE_PATH.open("w", encoding="utf-8") as f:
        json.dump(notices, f, ensure_ascii=False, indent=2)


def list_notices() -> list[dict]:
    with _STORE_LOCK:
        notices = _read_notices()
    notices.sort(key=lambda x: x.get("updated_at") or x.get("created_at") or "", reverse=True)
    return notices


def create_notice(title: str, content: str = "", enabled: bool = True) -> dict:
    with _STORE_LOCK:
        notices = _read_notices()
        now = datetime.now().isoformat()
        next_id = max([item.get("id", 0) for item in notices], default=0) + 1
        item = {
            "id": next_id,
            "title": title.strip(),
            "content": content.strip(),
            "enabled": bool(enabled),
            "created_at": now,
            "updated_at": now,
        }
        notices.append(item)
        _write_notices(notices)
    return item


def update_notice(notice_id: int, title: str, content: str = "", enabled: bool = True) -> dict | None:
    with _STORE_LOCK:
        notices = _read_notices()
        now = datetime.now().isoformat()
        for item in notices:
            if item.get("id") == notice_id:
                item["title"] = title.strip()
                item["content"] = content.strip()
                item["enabled"] = bool(enabled)
                item["updated_at"] = now
                _write_notices(notices)
                return item
    return None


def delete_notice(notice_id: int) -> bool:
    with _STORE_LOCK:
        notices = _read_notices()
        filtered = [item for item in notices if item.get("id") != notice_id]
        if len(filtered) == len(notices):
            return False
        _write_notices(filtered)
        return True

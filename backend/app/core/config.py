"""
配置加载器 - 从 config.yaml 读取配置
支持多 MySQL / Redis / AI 模型配置
"""

import os
import yaml
from pathlib import Path
from typing import Any, Optional

_config: dict = {}

CONFIG_DIR = Path(__file__).resolve().parent.parent.parent  # backend/
CONFIG_FILE = CONFIG_DIR / "config.yaml"


def _load_config() -> dict:
    """加载 YAML 配置"""
    global _config
    if _config:
        return _config

    config_path = os.environ.get("CONFIG_FILE", str(CONFIG_FILE))
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        _config = yaml.safe_load(f)
    return _config


def _get(*keys: str, default: Any = None) -> Any:
    """按路径取值，如 _get('mysql', 'default', 'host')"""
    cfg = _load_config()
    val = cfg
    for k in keys:
        if isinstance(val, dict):
            val = val.get(k)
        else:
            return default
        if val is None:
            return default
    return val


# ============================================================
# 应用配置
# ============================================================
APP_NAME: str = _get("app", "name", default="AgenticOps")
DEBUG: bool = _get("app", "debug", default=True)
VERSION: str = _get("app", "version", default="1.0.0")


# ============================================================
# MySQL 配置
# ============================================================
def get_mysql_url(name: str = "default") -> str:
    """获取 MySQL 连接 URL，name 对应 config.yaml 中 mysql 下的 key"""
    c = _get("mysql", name)
    if not c:
        raise KeyError(f"MySQL 配置 '{name}' 不存在")
    return (
        f"mysql+aiomysql://{c['user']}:{c['password']}"
        f"@{c['host']}:{c['port']}/{c['database']}"
    )


DATABASE_URL: str = get_mysql_url("default")


# ============================================================
# Redis 配置
# ============================================================
def get_redis_url(name: str = "default") -> str:
    """获取 Redis 连接 URL"""
    c = _get("redis", name)
    if not c:
        raise KeyError(f"Redis 配置 '{name}' 不存在")
    pwd = c.get("password")
    if pwd:
        return f"redis://:{pwd}@{c['host']}:{c['port']}/{c.get('db', 0)}"
    return f"redis://{c['host']}:{c['port']}/{c.get('db', 0)}"


REDIS_URL: str = get_redis_url("default")
REDIS_CACHE_PREFIX: str = _get("redis", "default", "cache_prefix", default="agenticops")


# ============================================================
# JWT 配置
# ============================================================
SECRET_KEY: str = _get("jwt", "secret_key", default="change-me")
ALGORITHM: str = _get("jwt", "algorithm", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = _get(
    "jwt", "access_token_expire_minutes", default=30
)
REFRESH_TOKEN_EXPIRE_DAYS: int = _get("jwt", "refresh_token_expire_days", default=7)


# ============================================================
# CORS 配置
# ============================================================
BACKEND_CORS_ORIGINS: list = _get("cors", "origins", default=["http://localhost:5173"])


# ============================================================
# AI 模型配置
# ============================================================
def get_ai_config(provider: str = "openai") -> dict:
    """获取 AI provider 配置"""
    c = _get("ai", provider)
    if not c:
        raise KeyError(f"AI 配置 '{provider}' 不存在")
    return c


def get_enabled_ai_providers() -> list[str]:
    """获取所有已启用的 AI provider 名称"""
    ai_cfg = _get("ai", default={})
    return [name for name, cfg in ai_cfg.items() if cfg.get("enabled")]

"""为 ops_scheduled_task 增加 updated_by 字段（幂等）"""

import asyncio
import os
import sys

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core import config


async def add_updated_by_column():
    engine = create_async_engine(config.DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        result = await conn.execute(text("SHOW COLUMNS FROM ops_scheduled_task LIKE 'updated_by'"))
        exists = result.first() is not None
        if exists:
            print("updated_by 字段已存在，无需处理")
        else:
            await conn.execute(
                text(
                    "ALTER TABLE ops_scheduled_task "
                    "ADD COLUMN updated_by VARCHAR(50) NULL COMMENT '修改人' AFTER created_by"
                )
            )
            print("已新增 updated_by 字段")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(add_updated_by_column())

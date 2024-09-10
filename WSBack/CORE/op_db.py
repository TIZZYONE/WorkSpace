#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Author: CC
@Date: {{DATE}}
"""
import asyncio
import json
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from sqlalchemy import MetaData, Table, insert,select,update
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
DATABASE_URI = "mysql+aiomysql://root:password@localhost/workspace"

async def open_db(table_name):
    # 创建数据库引擎
    engine = create_async_engine(DATABASE_URI)

    # 创建MetaData实例
    metadata = MetaData()

    # 反射现有的表
    async with engine.connect() as connection:
        await connection.run_sync(metadata.reflect)
        table = metadata.tables[table_name]

    return engine, table

treeList={
    "tree_list": [
        {"id": 100, "label": "新根节点", "children": []},
        {"id": 101, "label": "新根节点", "children": []},
        {"id": 102, "label": "新根节点", "children": []},
        {"id": 103, "label": "新根节点", "children": []}
    ],
    "create_people": "age111",
    "update_people": "cc"
}

async def execute_query(connection: AsyncConnection, query):
    try:
        result = await connection.execute(query)
        return result
    except SQLAlchemyError as e:
        logger.error(f"Database query failed: {e}")
        raise

async def main():
    # 打开数据库连接
    engine, table = await open_db('base_docs_data')
    try:
        # 使用异步上下文管理器创建数据库连接
        async with engine.connect() as connection:
            # 开始一个新的数据库事务
            async with connection.begin():
                    # 构建插入语句
                    ins = insert(table).values(
                        # tree_node=json.dumps(treeList["tree_list"]),  # 转换为JSON字符串
                        name='example_name',
                        columns="create_people",
                        savepeople="update_people",
                        tree_id ='111',
                        createtime=datetime.now()
                    )
                    # 执行插入语句
                    result = await connection.execute(ins)
                    # 提交事务
                    await connection.commit()
                    # 输出新插入记录的主键
                    print(result.inserted_primary_key)
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
    finally:
        # 关闭引擎
        await engine.dispose()



# 运行异步主函数
if __name__ == "__main__":
    asyncio.run(main())

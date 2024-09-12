#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Author: CC
@Date: {{DATE}}
"""

from typing import List, Dict, Any
import json
from fastapi import FastAPI, HTTPException, Body,Query
from sqlalchemy import create_engine, select, Table, Column, String, MetaData, Text, DateTime, Integer
from sqlalchemy.orm import Session, sessionmaker
from pydantic import BaseModel
import uvicorn
from CORE.op_db import open_db,execute_query
from fastapi import APIRouter
from sqlalchemy import insert,update,select
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

doc = APIRouter()

@doc.get("/GetData")
async def getData(treeid: str =Query(...)):
    # 打开数据库连接
    engine, table = await open_db('base_docs_data')
    try:
        # 使用异步上下文管理器创建数据库连接
        async with engine.connect() as connection:
            # 开始一个新的数据库事务
            async with connection.begin():
                sel = select(table).where(table.c.tree_id == str(treeid))
                # result = await connection.execute(sel)
                result = await execute_query(connection, sel)
                row = result.fetchone()

                if not row:
                    raise HTTPException(status_code=404, detail="Document not found")

                # 生成结果字典
                result_dict = {f"column{i}": row[i + 1] for i in range(0, 2) if row[i + 1]}
                print(result_dict)

                return result_dict

    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    finally:
        # 关闭引擎
        await engine.dispose()



class docsData(BaseModel):

    cls :List[Dict[str, List[str]]]
    datatext :str
    savepeople : str
    treeid : str
# [{'cls': ['cs1', 'cs2', 'cs3']}, {'cls2': ['css1', 'cs1s2']}]


@doc.post("/SubmitData")
async def submitData(data: docsData):
    print(data)
    # 打开数据库连接
    engine, table = await open_db('base_docs_data')
    try:
        # 使用异步上下文管理器创建数据库连接
        async with engine.connect() as connection:
            # 开始一个新的数据库事务
            async with connection.begin():
                sel = select(table).where(table.c.tree_id == data.treeid)
                # result = await connection.execute(sel)
                result = await execute_query(connection, sel)
                row = result.fetchone()
                if row:
                    upd = update(table).where(table.c.tree_id == data.treeid)
                    if data.cls is not None:
                        upd = upd.values(columns=str(data.cls))
                    if data.savepeople is not None:
                        upd = upd.values(savepeople=data.savepeople)
                    if data.datatext is not None:
                        upd = upd.values(text=data.datatext)
                    # result = await connection.execute(upd)
                    result = await execute_query(connection, upd)
                    print(f"Updated {result.rowcount} rows")
                else:
                    createtime = datetime.now()
                    print(createtime)
                    # 构建插入语句
                    ins = insert(table).values(
                        # tree_node=json.dumps(treeList["tree_list"]),  # 转换为JSON字符串
                        # name = data.name,
                        columns = str(data.cls),
                        createtime = str(createtime),
                        text =str(data.datatext),
                        savepeople = data.savepeople,
                        tree_id = data.treeid,
                    )
                    # 执行插入语句
                    # result = await connection.execute(ins)
                    result = await execute_query(connection, ins)
                    # 提交事务
                    await connection.commit()
                    # 输出新插入记录的主键
                    print(result.inserted_primary_key)

    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    finally:
        # 关闭引擎
        await engine.dispose()

@doc.get("/GetList")
async def getList(create_people:str):

    # 打开数据库连接
    engine, table = await open_db('base_docs_tree')
    try:
        # 使用异步上下文管理器创建数据库连接
        async with engine.connect() as connection:
            # 开始一个新的数据库事务
            async with connection.begin():
                sel = select(table).where(table.c.create_people == create_people)
                result = await connection.execute(sel)
                row = result.fetchone()
                if row:
                    # 构建字典
                    data = {
                        "id": row[0],
                        "tree_node": json.loads(row[1].replace("'", '"')),  # 将字符串转换为JSON对象
                        "create_people": row[2],
                        "update_people": row[3]
                    }

                    # 转换为JSON字符串
                    json_data = json.dumps(data, ensure_ascii=False, indent=4)
                    print(json_data)
                    return json_data
                else:
                    return {"message": "No data found"}

    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    finally:
        # 关闭引擎
        await engine.dispose()


class treeList(BaseModel):
    tree_list: List[Dict[str, Any]]
    create_people: str
    update_people: str


@doc.post("/SaveList")
async def saveList(treeList: treeList):
    # 打开数据库连接
    engine, table = await open_db('base_docs_tree')
    try:
        # 使用异步上下文管理器创建数据库连接
        async with engine.connect() as connection:
            # 开始一个新的数据库事务
            async with connection.begin():
                sel = select(table).where(table.c.create_people == treeList.create_people)
                result = await connection.execute(sel)
                row = result.fetchone()
                if row:
                    upd = update(table).where(table.c.create_people == treeList.create_people)
                    if treeList.tree_list is not None:
                        upd = upd.values(tree_node=str(treeList.tree_list))
                    if treeList.update_people is not None:
                        upd = upd.values(update_people=treeList.update_people)
                    result = await connection.execute(upd)
                    print(f"Updated {result.rowcount} rows")

                else:
                    # 构建插入语句
                    ins = insert(table).values(
                        # tree_node=json.dumps(treeList["tree_list"]),  # 转换为JSON字符串
                        tree_node=str(treeList.tree_list),
                        create_people=treeList.create_people,
                        update_people=treeList.update_people
                    )
                    # 执行插入语句
                    result = await connection.execute(ins)
                    # 提交事务
                    await connection.commit()
                    # 输出新插入记录的主键
                    print(result.inserted_primary_key)

    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    finally:
        # 关闭引擎
        await engine.dispose()

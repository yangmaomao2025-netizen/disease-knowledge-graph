"""
FastAPI 服务
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn

from src.extraction.triple_generator import triple_generator
from src.storage.neo4j_store import kg_store

app = FastAPI(
    title="专病知识图谱 API",
    description="医学知识图谱构建与查询服务",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求模型
class TextInput(BaseModel):
    text: str
    source: Optional[str] = None

class TripleInput(BaseModel):
    head: str
    head_type: str
    relation: str
    tail: str
    tail_type: str
    properties: Optional[Dict] = None

# API端点
@app.get("/")
def root():
    return {"message": "专病知识图谱 API", "version": "0.1.0"}

@app.post("/extract/triples")
def extract_triples(input: TextInput):
    """从文本提取三元组"""
    try:
        result = triple_generator.generate_from_text(input.text, input.source)
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/kg/add-triple")
def add_triple(triple: TripleInput):
    """添加三元组到知识图谱"""
    try:
        kg_store.add_triple(
            triple.head, triple.head_type,
            triple.relation,
            triple.tail, triple.tail_type,
            triple.properties
        )
        return {"success": True, "message": "三元组添加成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/kg/query")
def query_entity(
    name: str = Query(..., description="实体名称"),
    depth: int = Query(1, description="查询深度", ge=1, le=3)
):
    """查询实体相关知识"""
    try:
        results = kg_store.query_by_entity(name)
        return {
            "success": True,
            "entity": name,
            "count": len(results),
            "data": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/kg/statistics")
def get_statistics():
    """获取知识图谱统计信息"""
    try:
        stats = kg_store.get_statistics()
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/kg/path")
def find_path(
    start: str = Query(..., description="起始实体"),
    end: str = Query(..., description="目标实体"),
    max_depth: int = Query(3, description="最大深度", ge=1, le=5)
):
    """查找两实体间路径"""
    try:
        paths = kg_store.query_path(start, end, max_depth)
        return {
            "success": True,
            "start": start,
            "end": end,
            "path_count": len(paths),
            "data": paths
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

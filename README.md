# 专病知识图谱 (Disease Knowledge Graph)

医学专病知识图谱构建项目，支持临床决策、科研辅助和医学教育。

## 🎯 项目目标

构建面向特定疾病的结构化医学知识图谱，实现：
- 医学实体识别与关系抽取
- 知识图谱可视化
- 智能查询与推理
- API服务支持

## 🏗️ 技术架构

```
数据采集 → 知识抽取 → 知识融合 → 图存储 → API服务 → 可视化
    ↓           ↓           ↓          ↓          ↓          ↓
医学文献    NLP模型     实体对齐    Neo4j    FastAPI    D3.js
临床指南    规则引擎    知识推理   向量库    REST API   Vue3
```

## 📦 技术栈

| 组件 | 技术 |
|------|------|
| 图数据库 | Neo4j |
| 向量数据库 | Milvus |
| NLP | spaCy / BioBERT |
| 后端 | FastAPI |
| 前端 | Vue3 + D3.js |
| 部署 | Docker |

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动Neo4j
```bash
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:latest
```

### 3. 运行项目
```bash
python -m src.api.main
```

## 📁 项目结构

```
disease-knowledge-graph/
├── data/               # 数据文件
├── src/                # 源代码
├── models/             # NLP模型
├── notebooks/          # 分析 notebook
├── docs/               # 文档
└── tests/              # 测试
```

## 📚 文档

- [技术方案](./docs/tech-spec.md)
- [实体定义](./docs/entities.md)
- [关系定义](./docs/relations.md)
- [API文档](./docs/api.md)

## 📄 许可

MIT License

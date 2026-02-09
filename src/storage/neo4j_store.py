"""
知识图谱存储模块 - Neo4j图数据库操作
"""
from py2neo import Graph, Node, Relationship, NodeMatcher
from typing import List, Dict, Optional, Tuple
import os
from dotenv import load_dotenv

load_dotenv()

class KnowledgeGraphStore:
    """Neo4j知识图谱存储"""
    
    def __init__(self, uri=None, user=None, password=None):
        self.uri = uri or os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.user = user or os.getenv('NEO4J_USER', 'neo4j')
        self.password = password or os.getenv('NEO4J_PASSWORD', 'password')
        self.graph = Graph(self.uri, auth=(self.user, self.password))
        self.matcher = NodeMatcher(self.graph)
    
    def create_entity(self, entity_type: str, properties: Dict) -> Node:
        """创建实体节点"""
        node = Node(entity_type, **properties)
        self.graph.create(node)
        return node
    
    def get_entity(self, entity_type: str, name: str) -> Optional[Node]:
        """根据名称获取实体"""
        return self.matcher.match(entity_type, name=name).first()
    
    def create_relationship(self, from_node: Node, relation_type: str, to_node: Node, properties: Dict = None):
        """创建关系"""
        rel = Relationship(from_node, relation_type, to_node, **(properties or {}))
        self.graph.create(rel)
        return rel
    
    def add_triple(self, head_name: str, head_type: str, relation: str, tail_name: str, tail_type: str, properties: Dict = None):
        """添加三元组"""
        head = self.get_entity(head_type, head_name)
        if not head:
            head = self.create_entity(head_type, {'name': head_name})
        
        tail = self.get_entity(tail_type, tail_name)
        if not tail:
            tail = self.create_entity(tail_type, {'name': tail_name})
        
        return self.create_relationship(head, relation, tail, properties)
    
    def query_by_entity(self, entity_name: str) -> List[Dict]:
        """查询实体相关关系"""
        query = """
        MATCH (n)-[r]-(m)
        WHERE n.name = $name
        RETURN n, r, m
        """
        results = self.graph.run(query, name=entity_name).data()
        return results
    
    def query_path(self, start_name: str, end_name: str, max_depth: int = 3) -> List[Dict]:
        """查询两实体间路径"""
        query = """
        MATCH path = (start)-[*1..{max_depth}]-(end)
        WHERE start.name = $start_name AND end.name = $end_name
        RETURN path
        LIMIT 10
        """.format(max_depth=max_depth)
        return self.graph.run(query, start_name=start_name, end_name=end_name).data()
    
    def get_statistics(self) -> Dict:
        """获取图谱统计信息"""
        stats = {}
        
        # 实体数量
        entity_counts = self.graph.run("""
            MATCH (n)
            RETURN labels(n)[0] as type, count(*) as count
        """).data()
        stats['entities'] = {item['type']: item['count'] for item in entity_counts}
        
        # 关系数量
        relation_counts = self.graph.run("""
            MATCH ()-[r]-()
            RETURN type(r) as type, count(*) as count
        """).data()
        stats['relations'] = {item['type']: item['count'] for item in relation_counts}
        
        return stats
    
    def clear_graph(self):
        """清空图谱（慎用）"""
        self.graph.run("MATCH (n) DETACH DELETE n")

# 全局实例
kg_store = KnowledgeGraphStore()

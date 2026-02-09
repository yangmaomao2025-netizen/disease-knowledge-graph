"""
数据导入脚本 - 将三元组导入Neo4j
"""
import csv
import json
from pathlib import Path
from src.storage.neo4j_store import kg_store

def import_triples_from_csv(csv_path: str):
    """从CSV导入三元组"""
    count = 0
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                kg_store.add_triple(
                    head_name=row['head'],
                    head_type=row['head_type'],
                    relation=row['relation'],
                    tail_name=row['tail'],
                    tail_type=row['tail_type'],
                    properties={
                        'confidence': float(row.get('confidence', 0.5)),
                        'source': row.get('source', 'unknown')
                    }
                )
                count += 1
                if count % 10 == 0:
                    print(f"已导入 {count} 个三元组")
            except Exception as e:
                print(f"导入失败: {row} - {e}")
    
    return count

def import_entities_from_json(json_path: str):
    """从JSON导入实体"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count = 0
    for entity in data.get('entities', []):
        try:
            # 移除name字段作为属性
            entity_type = entity.pop('type', 'Entity')
            entity_name = entity.pop('name', '')
            
            # 创建实体
            kg_store.create_entity(entity_type, {
                'name': entity_name,
                **entity
            })
            count += 1
        except Exception as e:
            print(f"实体导入失败: {entity} - {e}")
    
    return count

def main():
    """主函数"""
    print("=== 知识图谱数据导入 ===\n")
    
    # 检查连接
    try:
        stats = kg_store.get_statistics()
        print(f"Neo4j连接成功")
        print(f"当前统计: {stats}\n")
    except Exception as e:
        print(f"Neo4j连接失败: {e}")
        print("请确保Neo4j已启动")
        return
    
    # 导入三元组
    triples_path = Path('data/processed/triples.csv')
    if triples_path.exists():
        print(f"导入三元组: {triples_path}")
        count = import_triples_from_csv(str(triples_path))
        print(f"✓ 导入完成: {count} 个三元组\n")
    else:
        print(f"文件不存在: {triples_path}")
    
    # 显示最终统计
    stats = kg_store.get_statistics()
    print("=== 导入后统计 ===")
    print(f"实体: {stats.get('entities', {})}")
    print(f"关系: {stats.get('relations', {})}")

if __name__ == '__main__':
    main()

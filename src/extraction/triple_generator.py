"""
三元组生成模块 - 从文本生成知识三元组
"""
from typing import List, Dict
from src.extraction.ner import ner_extractor
from src.extraction.relation import relation_extractor

class TripleGenerator:
    """知识三元组生成器"""
    
    def __init__(self):
        self.ner = ner_extractor
        self.relation_extractor = relation_extractor
    
    def generate_from_text(self, text: str, source: str = None) -> Dict:
        """从文本生成三元组"""
        # 1. 实体识别
        entities = self.ner.extract(text)
        
        # 2. 关系抽取
        relations = self.relation_extractor.extract(text, entities)
        
        # 3. 构建三元组
        triples = []
        for rel in relations:
            triples.append({
                'head': rel['head'],
                'head_type': rel['head_type'],
                'relation': rel['relation'],
                'tail': rel['tail'],
                'tail_type': rel['tail_type'],
                'confidence': rel.get('confidence', 0.5),
                'source': source or 'text'
            })
        
        return {
            'text': text,
            'entities': entities,
            'relations': relations,
            'triples': triples
        }
    
    def generate_from_texts(self, texts: List[str], source: str = None) -> List[Dict]:
        """批量生成三元组"""
        results = []
        for text in texts:
            result = self.generate_from_text(text, source)
            results.append(result)
        return results
    
    def export_triples(self, triples: List[Dict], format: str = 'csv') -> str:
        """导出三元组"""
        if format == 'csv':
            lines = ['head,head_type,relation,tail,tail_type,confidence,source']
            for t in triples:
                line = f"{t['head']},{t['head_type']},{t['relation']},{t['tail']},{t['tail_type']},{t.get('confidence', '')},{t.get('source', '')}"
                lines.append(line)
            return '\n'.join(lines)
        
        elif format == 'jsonl':
            import json
            return '\n'.join([json.dumps(t, ensure_ascii=False) for t in triples])
        
        else:
            raise ValueError(f"Unsupported format: {format}")

# 全局实例
triple_generator = TripleGenerator()

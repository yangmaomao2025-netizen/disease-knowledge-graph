"""
关系抽取模块 - 医学关系识别
"""
from typing import List, Dict, Tuple
import re

class RelationExtractor:
    """医学关系抽取器"""
    
    # 关系模式定义（规则匹配）
    RELATION_PATTERNS = {
        'TREATED_BY': {
            'keywords': ['治疗', '用于', '适用于', '用药'],
            'patterns': [
                r'{disease}.*?(?:治疗|用于).*?{drug}',
                r'{drug}.*?(?:治疗|用于).*?{disease}'
            ]
        },
        'HAS_SYMPTOM': {
            'keywords': ['表现为', '症状', '出现'],
            'patterns': [
                r'{disease}.*?(?:表现为|症状).*?{symptom}',
                r'{symptom}.*?(?:见于|是).*?{disease}.*?症状'
            ]
        },
        'DIAGNOSED_BY': {
            'keywords': ['诊断', '检查', '通过'],
            'patterns': [
                r'{disease}.*?(?:诊断|检查).*?{examination}',
                r'{examination}.*?(?:诊断|用于).*?{disease}'
            ]
        },
        'CAUSES': {
            'keywords': ['导致', '引起', '造成'],
            'patterns': [
                r'{drug}.*?(?:导致|引起|造成).*?{symptom}'
            ]
        },
        'CONTRAINDICATED_WITH': {
            'keywords': ['禁忌', '禁用', '不能合用'],
            'patterns': [
                r'{drug}.*?禁忌.*?{drug2}',
                r'{drug}.*?不能与.*?{drug2}.*?合用'
            ]
        }
    }
    
    # 实体类型到关系类型的映射
    ENTITY_RELATION_MAP = {
        ('DISEASE', 'DRUG'): ['TREATED_BY', 'FIRST_LINE', 'SECOND_LINE'],
        ('DISEASE', 'SYMPTOM'): ['HAS_SYMPTOM', 'COMMON_SYMPTOM'],
        ('DISEASE', 'EXAMINATION'): ['DIAGNOSED_BY', 'CONFIRMED_BY'],
        ('DRUG', 'SYMPTOM'): ['RELIEVES', 'CAUSES'],
        ('DRUG', 'DRUG'): ['INTERACTS_WITH', 'CONTRAINDICATED_WITH'],
        ('DISEASE', 'DISEASE'): ['COMPLICATION', 'DIFFERENTIAL']
    }
    
    def __init__(self):
        self.patterns = self.RELATION_PATTERNS
    
    def extract_by_rules(self, text: str, entities: List[Dict]) -> List[Dict]:
        """基于规则抽取关系"""
        relations = []
        
        # 构建实体位置索引
        entity_map = {}
        for i, ent in enumerate(entities):
            key = (ent['start'], ent['end'])
            entity_map[key] = ent
        
        # 遍历实体对
        for i, head in enumerate(entities):
            for j, tail in enumerate(entities):
                if i == j:
                    continue
                
                # 检查实体对是否支持关系
                relation_types = self.ENTITY_RELATION_MAP.get(
                    (head['type'], tail['type']), []
                )
                
                for rel_type in relation_types:
                    # 检查文本中是否有关系关键词
                    between_text = text[head['end']:tail['start']]
                    
                    if rel_type in self.patterns:
                        keywords = self.patterns[rel_type].get('keywords', [])
                        if any(kw in between_text for kw in keywords):
                            relations.append({
                                'head': head['text'],
                                'head_type': head['type'],
                                'relation': rel_type,
                                'tail': tail['text'],
                                'tail_type': tail['type'],
                                'confidence': 0.7,
                                'source': 'rule'
                            })
        
        return relations
    
    def extract_by_patterns(self, text: str, entities: List[Dict]) -> List[Dict]:
        """基于正则模式抽取关系"""
        relations = []
        
        # 简化实现 - 实际项目需要更复杂的模式匹配
        # 这里仅作为示例
        
        return relations
    
    def extract(self, text: str, entities: List[Dict]) -> List[Dict]:
        """抽取关系"""
        relations = []
        
        # 规则抽取
        relations.extend(self.extract_by_rules(text, entities))
        
        # 去重
        seen = set()
        unique_relations = []
        for rel in relations:
            key = (rel['head'], rel['relation'], rel['tail'])
            if key not in seen:
                seen.add(key)
                unique_relations.append(rel)
        
        return unique_relations

# 全局实例
relation_extractor = RelationExtractor()

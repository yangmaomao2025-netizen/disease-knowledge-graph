"""
实体识别模块 - 医学NER
"""
import spacy
from typing import List, Dict, Tuple
import re

class MedicalNER:
    """医学实体识别器"""
    
    # 实体类型定义
    ENTITY_TYPES = {
        'DISEASE': '疾病',
        'SYMPTOM': '症状',
        'DRUG': '药物',
        'EXAMINATION': '检查',
        'TREATMENT': '治疗方案',
        'ANATOMY': '解剖部位',
        'GENE': '基因/蛋白'
    }
    
    def __init__(self, model_name='en_core_sci_sm'):
        """初始化NER模型"""
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            print(f"模型 {model_name} 未找到，使用基础规则匹配")
            self.nlp = None
        
        # 加载医学词典（简化版）
        self.dictionaries = self._load_dictionaries()
    
    def _load_dictionaries(self) -> Dict[str, List[str]]:
        """加载医学词典"""
        # 实际项目中从文件加载
        return {
            'DISEASE': ['肺癌', '糖尿病', '高血压', '冠心病', '脑卒中'],
            'SYMPTOM': ['咳嗽', '发热', '胸痛', '呼吸困难', '头痛'],
            'DRUG': ['吉非替尼', '奥希替尼', '二甲双胍', '阿司匹林'],
            'EXAMINATION': ['CT', 'MRI', 'X光', '血常规', '活检'],
            'ANATOMY': ['肺', '心脏', '肝脏', '脑部', '胃']
        }
    
    def extract_by_rules(self, text: str) -> List[Dict]:
        """基于规则提取实体"""
        entities = []
        
        for entity_type, keywords in self.dictionaries.items():
            for keyword in keywords:
                for match in re.finditer(re.escape(keyword), text):
                    entities.append({
                        'text': keyword,
                        'type': entity_type,
                        'start': match.start(),
                        'end': match.end(),
                        'source': 'rule'
                    })
        
        # 去重（按位置）
        entities = sorted(entities, key=lambda x: (x['start'], -x['end']))
        filtered = []
        for e in entities:
            if not any(f['start'] <= e['start'] and f['end'] >= e['end'] for f in filtered):
                filtered.append(e)
        
        return filtered
    
    def extract_by_model(self, text: str) -> List[Dict]:
        """基于模型提取实体"""
        if self.nlp is None:
            return []
        
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'type': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char,
                'source': 'model'
            })
        
        return entities
    
    def extract(self, text: str, use_rules=True, use_model=True) -> List[Dict]:
        """提取实体（融合规则和模型）"""
        all_entities = []
        
        if use_rules:
            all_entities.extend(self.extract_by_rules(text))
        
        if use_model and self.nlp:
            all_entities.extend(self.extract_by_model(text))
        
        # 合并和去重
        all_entities = sorted(all_entities, key=lambda x: (x['start'], -x['end']))
        filtered = []
        for e in all_entities:
            if not any(f['start'] <= e['start'] and f['end'] >= e['end'] for f in filtered):
                filtered.append(e)
        
        return filtered

# 全局实例
ner_extractor = MedicalNER()

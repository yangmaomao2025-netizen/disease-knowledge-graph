"""
数据采集模块 - 公开医学数据集下载与预处理
"""
import json
import csv
import requests
from typing import List, Dict
from pathlib import Path

class DataCollector:
    """医学数据采集器"""
    
    # 目标慢病
    TARGET_DISEASES = [
        '高血压', 'Hypertension',
        '糖尿病', 'Diabetes', '2型糖尿病', 'T2DM',
        '冠心病', 'Coronary Heart Disease', 'CHD',
        '慢性阻塞性肺疾病', 'COPD', '慢阻肺',
        '脑卒中', 'Stroke', '中风',
        '慢性肾病', 'CKD', 'Chronic Kidney Disease'
    ]
    
    def __init__(self, data_dir: str = './data'):
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / 'raw'
        self.processed_dir = self.data_dir / 'processed'
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_demo_data(self) -> Dict:
        """生成演示数据（慢病知识）"""
        data = {
            'entities': [],
            'relations': []
        }
        
        # 疾病实体
        diseases = [
            {
                'name': '2型糖尿病',
                'type': 'DISEASE',
                'aliases': ['T2DM', 'Type 2 Diabetes', '成人糖尿病'],
                'icd10': 'E11',
                'definition': '以胰岛素抵抗和相对胰岛素缺乏为特征的慢性代谢性疾病',
                'category': '内分泌代谢疾病',
                'risk_factors': ['肥胖', '家族史', '不良饮食习惯', '缺乏运动'],
                'complications': ['糖尿病肾病', '糖尿病视网膜病变', '心血管疾病']
            },
            {
                'name': '高血压',
                'type': 'DISEASE',
                'aliases': ['Hypertension', 'HTN'],
                'icd10': 'I10',
                'definition': '以体循环动脉血压持续升高为主要特征的慢性疾病',
                'category': '心血管疾病',
                'risk_factors': ['高盐饮食', '肥胖', '吸烟', '饮酒', '精神紧张'],
                'complications': ['脑卒中', '冠心病', '心力衰竭', '肾功能不全']
            },
            {
                'name': '冠心病',
                'type': 'DISEASE',
                'aliases': ['Coronary Heart Disease', 'CHD', '冠状动脉粥样硬化性心脏病'],
                'icd10': 'I25',
                'definition': '冠状动脉粥样硬化导致心肌缺血缺氧的心脏病',
                'category': '心血管疾病',
                'risk_factors': ['高血压', '高血脂', '糖尿病', '吸烟', '肥胖'],
                'complications': ['心肌梗死', '心力衰竭', '心律失常']
            },
            {
                'name': '慢性阻塞性肺疾病',
                'type': 'DISEASE',
                'aliases': ['COPD', '慢阻肺'],
                'icd10': 'J44',
                'definition': '以持续气流受限为特征的慢性肺部疾病',
                'category': '呼吸系统疾病',
                'risk_factors': ['吸烟', '空气污染', '职业粉尘', '遗传因素'],
                'complications': ['肺心病', '呼吸衰竭', '自发性气胸']
            },
            {
                'name': '脑卒中',
                'type': 'DISEASE',
                'aliases': ['Stroke', '中风', '脑血管意外'],
                'icd10': 'I64',
                'definition': '急性脑血管循环障碍导致的脑功能损害',
                'category': '神经系统疾病',
                'risk_factors': ['高血压', '房颤', '糖尿病', '高血脂', '吸烟'],
                'complications': ['偏瘫', '失语', '吞咽困难', '认知障碍']
            },
            {
                'name': '慢性肾病',
                'type': 'DISEASE',
                'aliases': ['CKD', 'Chronic Kidney Disease', '慢性肾功能不全'],
                'icd10': 'N18',
                'definition': '肾脏结构或功能异常持续超过3个月',
                'category': '泌尿系统疾病',
                'risk_factors': ['糖尿病', '高血压', '肾小球肾炎', '多囊肾'],
                'complications': ['肾衰竭', '心血管疾病', '贫血', '骨病']
            }
        ]
        
        # 药物实体
        drugs = [
            {
                'name': '二甲双胍',
                'type': 'DRUG',
                'category': '双胍类降糖药',
                'indications': ['2型糖尿病'],
                'contraindications': ['严重肾功能不全', '酸中毒', '严重感染'],
                'side_effects': ['胃肠道反应', '维生素B12缺乏', '乳酸酸中毒(罕见)']
            },
            {
                'name': '氨氯地平',
                'type': 'DRUG',
                'category': '钙通道阻滞剂',
                'indications': ['高血压', '心绞痛'],
                'contraindications': ['严重低血压', '心源性休克'],
                'side_effects': ['踝部水肿', '头痛', '面部潮红']
            },
            {
                'name': '阿司匹林',
                'type': 'DRUG',
                'category': '抗血小板药',
                'indications': ['冠心病', '脑卒中预防', '心绞痛'],
                'contraindications': ['活动性出血', '血友病', '阿司匹林哮喘'],
                'side_effects': ['胃肠道出血', '过敏反应', '耳鸣']
            },
            {
                'name': '沙美特罗',
                'type': 'DRUG',
                'category': '长效β2受体激动剂',
                'indications': ['COPD', '哮喘'],
                'contraindications': ['对成分过敏'],
                'side_effects': ['震颤', '心悸', '低钾血症']
            },
            {
                'name': '阿托伐他汀',
                'type': 'DRUG',
                'category': '他汀类降脂药',
                'indications': ['高胆固醇血症', '冠心病二级预防'],
                'contraindications': ['活动性肝病', '妊娠期'],
                'side_effects': ['肌肉痛', '肝酶升高', '糖尿病风险增加']
            }
        ]
        
        # 症状实体
        symptoms = [
            {'name': '多饮', 'type': 'SYMPTOM'},
            {'name': '多尿', 'type': 'SYMPTOM'},
            {'name': '体重下降', 'type': 'SYMPTOM'},
            {'name': '乏力', 'type': 'SYMPTOM'},
            {'name': '头痛', 'type': 'SYMPTOM'},
            {'name': '头晕', 'type': 'SYMPTOM'},
            {'name': '胸痛', 'type': 'SYMPTOM'},
            {'name': '胸闷', 'type': 'SYMPTOM'},
            {'name': '呼吸困难', 'type': 'SYMPTOM'},
            {'name': '慢性咳嗽', 'type': 'SYMPTOM'},
            {'name': '咳痰', 'type': 'SYMPTOM'},
            {'name': '偏瘫', 'type': 'SYMPTOM'},
            {'name': '言语不清', 'type': 'SYMPTOM'},
            {'name': '水肿', 'type': 'SYMPTOM'},
            {'name': '蛋白尿', 'type': 'SYMPTOM'}
        ]
        
        # 检查实体
        examinations = [
            {'name': '空腹血糖', 'type': 'EXAMINATION', 'normal_range': '3.9-6.1 mmol/L'},
            {'name': '糖化血红蛋白', 'type': 'EXAMINATION', 'normal_range': '<6.5%'},
            {'name': '血压测量', 'type': 'EXAMINATION', 'normal_range': '<140/90 mmHg'},
            {'name': '心电图', 'type': 'EXAMINATION'},
            {'name': '胸部CT', 'type': 'EXAMINATION'},
            {'name': '肺功能检查', 'type': 'EXAMINATION'},
            {'name': '头颅CT', 'type': 'EXAMINATION'},
            {'name': '肾功能检查', 'type': 'EXAMINATION'},
            {'name': '尿常规', 'type': 'EXAMINATION'},
            {'name': '血脂检查', 'type': 'EXAMINATION'}
        ]
        
        data['entities'] = diseases + drugs + symptoms + examinations
        
        # 关系三元组
        relations = [
            # 疾病-症状
            ('2型糖尿病', 'DISEASE', 'HAS_SYMPTOM', '多饮', 'SYMPTOM'),
            ('2型糖尿病', 'DISEASE', 'HAS_SYMPTOM', '多尿', 'SYMPTOM'),
            ('2型糖尿病', 'DISEASE', 'HAS_SYMPTOM', '体重下降', 'SYMPTOM'),
            ('2型糖尿病', 'DISEASE', 'HAS_SYMPTOM', '乏力', 'SYMPTOM'),
            ('高血压', 'DISEASE', 'HAS_SYMPTOM', '头痛', 'SYMPTOM'),
            ('高血压', 'DISEASE', 'HAS_SYMPTOM', '头晕', 'SYMPTOM'),
            ('冠心病', 'DISEASE', 'HAS_SYMPTOM', '胸痛', 'SYMPTOM'),
            ('冠心病', 'DISEASE', 'HAS_SYMPTOM', '胸闷', 'SYMPTOM'),
            ('慢性阻塞性肺疾病', 'DISEASE', 'HAS_SYMPTOM', '呼吸困难', 'SYMPTOM'),
            ('慢性阻塞性肺疾病', 'DISEASE', 'HAS_SYMPTOM', '慢性咳嗽', 'SYMPTOM'),
            ('慢性阻塞性肺疾病', 'DISEASE', 'HAS_SYMPTOM', '咳痰', 'SYMPTOM'),
            ('脑卒中', 'DISEASE', 'HAS_SYMPTOM', '偏瘫', 'SYMPTOM'),
            ('脑卒中', 'DISEASE', 'HAS_SYMPTOM', '言语不清', 'SYMPTOM'),
            ('慢性肾病', 'DISEASE', 'HAS_SYMPTOM', '水肿', 'SYMPTOM'),
            ('慢性肾病', 'DISEASE', 'HAS_SYMPTOM', '蛋白尿', 'SYMPTOM'),
            
            # 疾病-药物
            ('2型糖尿病', 'DISEASE', 'TREATED_BY', '二甲双胍', 'DRUG'),
            ('2型糖尿病', 'DISEASE', 'FIRST_LINE', '二甲双胍', 'DRUG'),
            ('高血压', 'DISEASE', 'TREATED_BY', '氨氯地平', 'DRUG'),
            ('高血压', 'DISEASE', 'FIRST_LINE', '氨氯地平', 'DRUG'),
            ('冠心病', 'DISEASE', 'TREATED_BY', '阿司匹林', 'DRUG'),
            ('冠心病', 'DISEASE', 'FIRST_LINE', '阿司匹林', 'DRUG'),
            ('脑卒中', 'DISEASE', 'TREATED_BY', '阿司匹林', 'DRUG'),
            ('慢性阻塞性肺疾病', 'DISEASE', 'TREATED_BY', '沙美特罗', 'DRUG'),
            ('冠心病', 'DISEASE', 'TREATED_BY', '阿托伐他汀', 'DRUG'),
            
            # 疾病-检查
            ('2型糖尿病', 'DISEASE', 'DIAGNOSED_BY', '空腹血糖', 'EXAMINATION'),
            ('2型糖尿病', 'DISEASE', 'DIAGNOSED_BY', '糖化血红蛋白', 'EXAMINATION'),
            ('高血压', 'DISEASE', 'DIAGNOSED_BY', '血压测量', 'EXAMINATION'),
            ('冠心病', 'DISEASE', 'DIAGNOSED_BY', '心电图', 'EXAMINATION'),
            ('慢性阻塞性肺疾病', 'DISEASE', 'DIAGNOSED_BY', '肺功能检查', 'EXAMINATION'),
            ('脑卒中', 'DISEASE', 'DIAGNOSED_BY', '头颅CT', 'EXAMINATION'),
            ('慢性肾病', 'DISEASE', 'DIAGNOSED_BY', '肾功能检查', 'EXAMINATION'),
            ('慢性肾病', 'DISEASE', 'DIAGNOSED_BY', '尿常规', 'EXAMINATION'),
            
            # 药物-副作用
            ('二甲双胍', 'DRUG', 'CAUSES', '胃肠道反应', 'SYMPTOM'),
            ('阿司匹林', 'DRUG', 'CAUSES', '胃肠道出血', 'SYMPTOM'),
            ('氨氯地平', 'DRUG', 'CAUSES', '踝部水肿', 'SYMPTOM'),
            
            # 疾病-并发症
            ('2型糖尿病', 'DISEASE', 'COMPLICATION', '慢性肾病', 'DISEASE'),
            ('2型糖尿病', 'DISEASE', 'COMPLICATION', '冠心病', 'DISEASE'),
            ('高血压', 'DISEASE', 'COMPLICATION', '脑卒中', 'DISEASE'),
            ('高血压', 'DISEASE', 'COMPLICATION', '冠心病', 'DISEASE'),
            ('高血压', 'DISEASE', 'COMPLICATION', '慢性肾病', 'DISEASE'),
        ]
        
        for head, head_type, relation, tail, tail_type in relations:
            data['relations'].append({
                'head': head,
                'head_type': head_type,
                'relation': relation,
                'tail': tail,
                'tail_type': tail_type,
                'confidence': 0.95,
                'source': 'demo_data'
            })
        
        return data
    
    def save_to_json(self, data: Dict, filename: str = 'medical_data.json'):
        """保存为JSON"""
        filepath = self.processed_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filepath
    
    def save_triples_to_csv(self, relations: List[Dict], filename: str = 'triples.csv'):
        """保存三元组为CSV"""
        filepath = self.processed_dir / filename
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['head', 'head_type', 'relation', 'tail', 'tail_type', 'confidence', 'source'])
            for rel in relations:
                writer.writerow([
                    rel['head'], rel['head_type'], rel['relation'],
                    rel['tail'], rel['tail_type'],
                    rel.get('confidence', ''), rel.get('source', '')
                ])
        return filepath
    
    def save_entities_to_csv(self, entities: List[Dict], filename: str = 'entities.csv'):
        """保存实体为CSV"""
        filepath = self.processed_dir / filename
        
        # 获取所有字段
        fields = set()
        for ent in entities:
            fields.update(ent.keys())
        fields = sorted(fields)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for ent in entities:
                writer.writerow(ent)
        
        return filepath

# 全局实例
data_collector = DataCollector()

if __name__ == '__main__':
    # 生成演示数据
    print("生成慢病演示数据...")
    data = data_collector.generate_demo_data()
    
    # 保存数据
    json_path = data_collector.save_to_json(data)
    print(f"JSON数据已保存: {json_path}")
    
    triples_path = data_collector.save_triples_to_csv(data['relations'])
    print(f"三元组已保存: {triples_path}")
    
    entities_path = data_collector.save_entities_to_csv(data['entities'])
    print(f"实体已保存: {entities_path}")
    
    print(f"\n数据统计:")
    print(f"- 实体数量: {len(data['entities'])}")
    print(f"- 关系数量: {len(data['relations'])}")
    print(f"- 疾病: {len([e for e in data['entities'] if e['type'] == 'DISEASE'])}")
    print(f"- 药物: {len([e for e in data['entities'] if e['type'] == 'DRUG'])}")
    print(f"- 症状: {len([e for e in data['entities'] if e['type'] == 'SYMPTOM'])}")
    print(f"- 检查: {len([e for e in data['entities'] if e['type'] == 'EXAMINATION'])}")

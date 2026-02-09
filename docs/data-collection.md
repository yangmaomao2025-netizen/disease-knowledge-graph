# 常见慢病知识图谱 - 数据收集与整理

## 慢病范围确定

### 目标慢病（6种核心疾病）
1. **高血压 (Hypertension)**
2. **2型糖尿病 (Type 2 Diabetes)**
3. **冠心病 (Coronary Heart Disease)**
4. **慢性阻塞性肺疾病/COPD**
5. **脑卒中/中风 (Stroke)**
6. **慢性肾病 (Chronic Kidney Disease)**

## 公开数据源调研

### 1. 中文数据源

#### CMeKG (中文医学知识图谱)
- **网址**: https://github.com/kingzhu/cmeg
- **内容**: 疾病、症状、药物、治疗等实体和关系
- **格式**: JSON/CSV
- **许可**: 开放使用
- **适用**: 基础医学实体和关系

#### 医学百科 (WikiMed)
- **来源**: 百度百科医学词条 + 维基百科
- **内容**: 疾病定义、症状、治疗
- **获取**: 爬虫或API
- **适用**: 实体属性和描述

#### 国家卫健委临床路径
- **来源**: 卫健委官网
- **内容**: 标准化诊疗方案
- **格式**: PDF/文档
- **适用**: 治疗方案实体

#### 药典数据
- **来源**: 中国药典
- **内容**: 药物信息、适应症、禁忌
- **适用**: 药物实体

### 2. 英文数据源

#### UMLS (Unified Medical Language System)
- **网址**: https://www.nlm.nih.gov/research/umls/
- **内容**: 医学术语、概念、关系
- **需要**: 申请许可
- **适用**: 术语标准化

#### SNOMED CT
- **网址**: https://www.snomed.org/
- **内容**: 临床术语系统
- **需要**: 会员资格
- **适用**: 实体标准化

#### DrugBank
- **网址**: https://go.drugbank.com/
- **内容**: 药物信息、相互作用
- **许可**: 开放数据许可
- **适用**: 药物实体和关系

#### MIMIC-III (临床数据)
- **网址**: https://physionet.org/content/mimiciii/
- **内容**: 去标识化临床记录
- **需要**: 培训认证
- **适用**: 真实临床场景验证

### 3. 专科数据源

#### 心血管
- AHA/ACC指南
- 中国心血管健康联盟

#### 糖尿病
- ADA指南
- CDS指南

#### 呼吸
- GOLD指南 (COPD)
- GINA指南 (哮喘)

## 数据采集策略

### 阶段1: 快速启动 (使用开放数据)
1. CMeKG基础数据
2. 医学百科词条
3. DrugBank药物数据

### 阶段2: 深度补充
1. 临床指南解析
2. 医学文献抽取
3. 专家知识校验

## 实体数据结构设计

### 疾病实体示例
```json
{
  "name": "2型糖尿病",
  "aliases": ["T2DM", "Type 2 Diabetes", "成人糖尿病"],
  "icd10": "E11",
  "definition": "以胰岛素抵抗和相对胰岛素缺乏为特征的代谢性疾病...",
  "category": "内分泌代谢疾病",
  "risk_factors": ["肥胖", "家族史", "不良饮食习惯"],
  "prevalence": "0.11",
  "source": "CMeKG"
}
```

### 药物实体示例
```json
{
  "name": "二甲双胍",
  "generic_name": "Metformin",
  "brand_names": ["格华止", "迪化唐锭"],
  "category": "双胍类降糖药",
  "indications": ["2型糖尿病", "多囊卵巢综合征"],
  "contraindications": ["严重肾功能不全", "酸中毒"],
  "side_effects": ["胃肠道反应", "维生素B12缺乏"],
  "dosage": "起始500mg bid，最大2550mg/日",
  "source": "DrugBank"
}
```

## 三元组数据格式

### CSV格式
```csv
head,head_type,relation,tail,tail_type,confidence,source
2型糖尿病,DISEASE,TREATED_BY,二甲双胍,DRUG,0.95,CMeKG
2型糖尿病,DISEASE,HAS_SYMPTOM,多饮,SYMPTOM,0.90,医学百科
二甲双胍,DRUG,CAUSES,胃肠道反应,SYMPTOM,0.85,DrugBank
```

### JSON格式
```json
{
  "triples": [
    {
      "head": "2型糖尿病",
      "head_type": "DISEASE",
      "relation": "TREATED_BY",
      "tail": "二甲双胍",
      "tail_type": "DRUG",
      "confidence": 0.95,
      "source": "CMeKG"
    }
  ]
}
```

## 下一步行动

1. 下载CMeKG数据
2. 提取慢病相关子集
3. 整理标准化实体
4. 生成三元组文件
5. 导入Neo4j图谱

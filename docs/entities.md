# 实体定义

## 疾病 (Disease)

| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| name | string | 疾病名称 | 非小细胞肺癌 |
| aliases | list | 别名 | ["NSCLC", "Non-small cell lung cancer"] |
| icd10 | string | ICD-10编码 | C34.9 |
| definition | text | 疾病定义 | ... |
| category | string | 分类 | 恶性肿瘤 |
| incidence | float | 发病率 | 0.05 |
| system | string | 所属系统 | 呼吸系统 |

## 症状 (Symptom)

| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| name | string | 症状名称 | 咳嗽 |
| commonness | enum | 常见程度 | common/uncommon/rare |
| description | text | 特征描述 | 持续性干咳 |

## 药物 (Drug)

| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| generic_name | string | 通用名 | 吉非替尼 |
| brand_names | list | 商品名 | ["易瑞沙", "Iressa"] |
| category | string | 药理分类 | EGFR抑制剂 |
| indications | list | 适应症 | ["NSCLC"] |
| contraindications | list | 禁忌症 | [...] |
| side_effects | list | 不良反应 | ["皮疹", "腹泻"] |

## 检查 (Examination)

| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| name | string | 检查名称 | 胸部CT |
| type | enum | 检查类型 | imaging |
| normal_range | string | 正常值 | ... |
| clinical_significance | text | 临床意义 | ... |

## 治疗方案 (Treatment)

| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| name | string | 方案名称 | 肺叶切除术 |
| type | enum | 治疗类型 | surgery |
| indications | list | 适应症 | ["早期NSCLC"] |
| contraindications | list | 禁忌症 | [...] |

## 解剖部位 (Anatomy)

| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| name | string | 部位名称 | 右肺上叶 |
| system | string | 系统分类 | 呼吸系统 |
| function | text | 功能描述 | 气体交换 |

## 基因/蛋白 (Gene)

| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| name | string | 基因名称 | EGFR |
| symbol | string | 基因符号 | EGFR |
| function | text | 功能描述 | 受体酪氨酸激酶 |
| related_diseases | list | 相关疾病 | ["NSCLC"] |

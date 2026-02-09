# 关系定义

## 疾病-症状关系

| 关系 | 说明 | 示例 |
|------|------|------|
| HAS_SYMPTOM | 表现为 | 肺癌-HAS_SYMPTOM-咳嗽 |
| COMMON_SYMPTOM | 常见症状 | 肺癌-COMMON_SYMPTOM-咳血 |
| RARE_SYMPTOM | 罕见症状 | 肺癌-RARE_SYMPTOM-声音嘶哑 |

## 疾病-药物关系

| 关系 | 说明 | 示例 |
|------|------|------|
| TREATED_BY | 治疗用药 | 肺癌-TREATED_BY-吉非替尼 |
| FIRST_LINE | 一线用药 | NSCLC-FIRST_LINE-奥希替尼 |
| SECOND_LINE | 二线用药 | NSCLC-SECOND_LINE-多西他赛 |

## 疾病-检查关系

| 关系 | 说明 | 示例 |
|------|------|------|
| DIAGNOSED_BY | 辅助诊断 | 肺癌-DIAGNOSED_BY-胸部CT |
| CONFIRMED_BY | 确诊检查 | 肺癌-CONFIRMED_BY-活检 |
| SCREENED_BY | 筛查手段 | 肺癌-SCREENED_BY-低剂量CT |

## 疾病-疾病关系

| 关系 | 说明 | 示例 |
|------|------|------|
| COMPLICATION | 并发症 | 肺癌-COMPLICATION-胸腔积液 |
| DIFFERENTIAL | 鉴别诊断 | 肺癌-DIFFERENTIAL-肺结核 |
| RELATED_TO | 相关疾病 | 肺癌-RELATED_TO-慢阻肺 |

## 药物-药物关系

| 关系 | 说明 | 示例 |
|------|------|------|
| INTERACTS_WITH | 相互作用 | 吉非替尼-INTERACTS_WITH-华法林 |
| COMBINED_WITH | 联合用药 | 培美曲塞-COMBINED_WITH-顺铂 |
| CONTRAINDICATED_WITH | 禁忌联用 | ... |

## 药物-症状关系

| 关系 | 说明 | 示例 |
|------|------|------|
| RELIEVES | 缓解 | 吗啡-RELIEVES-疼痛 |
| CAUSES | 导致 | 吉非替尼-CAUSES-皮疹 |

## 检查-疾病关系

| 关系 | 说明 | 示例 |
|------|------|------|
| INDICATES | 提示 | CEA升高-INDICATES-肺癌 |
| EXCLUDES | 排除 | 活检阴性-EXCLUDES-恶性肿瘤 |

## 治疗方案-疾病关系

| 关系 | 说明 | 示例 |
|------|------|------|
| STANDARD_FOR | 标准治疗 | 手术-STANDARD_FOR-早期肺癌 |
| ALTERNATIVE_FOR | 替代治疗 | 放疗-ALTERNATIVE_FOR-不可手术肺癌 |

## 基因-疾病关系

| 关系 | 说明 | 示例 |
|------|------|------|
| SUSCEPTIBILITY_GENE | 易感基因 | EGFR突变-SUSCEPTIBILITY_GENE-肺腺癌 |
| PATHOGENIC_GENE | 致病基因 | ALK融合-PATHOGENIC_GENE-NSCLC |
| BIOMARKER_FOR | 生物标志物 | PD-L1-BIOMARKER_FOR-免疫治疗 |

## 解剖-疾病关系

| 关系 | 说明 | 示例 |
|------|------|------|
| LOCATED_IN | 发病部位 | 肺癌-LOCATED_IN-右肺上叶 |
| SPREADS_TO | 转移部位 | 肺癌-SPREADS_TO-脑 |

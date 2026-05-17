import yaml
import os

# Yeh teen lines kisi bhi folder se config file ka exact absolute path nikal lengi
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "gateway_config.yaml")

# Ab file os.path ke exact system absolute route se read hogi
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

def evaluate_gateway_policy(rule_score: float, semantic_score: float, pii_entities: list) -> tuple:
    r_w = config["thresholds"]["rule_weight"]
    s_w = config["thresholds"]["semantic_weight"]
    
    # Lab Final justified risk calculation formula (Weighted Average)
    final_risk = (rule_score * r_w) + (semantic_score * s_w)
    
    # 1. Agar risk threshold se zyada ho ya direct match ho jaye to BLOCK karein
    if final_risk >= config["thresholds"]["block_threshold"] or rule_score >= 0.80:
        return round(final_risk, 2), "BLOCK", ["INJECTION_ATTEMPT"]
        
    # 2. Agar risk low ho lekin sensitive data (PII) maujood ho to MASK karein
    if len(pii_entities) > 0:
        return round(final_risk, 2), "MASK", ["SENSITIVE_DATA_LEAKAGE"]
        
    # 3. Agar sab kuch bilkul safe ho to ALLOW karein
    return round(final_risk, 2), "ALLOW", ["ALL_CLEAR"]
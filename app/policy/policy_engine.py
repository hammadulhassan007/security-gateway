import yaml
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "gateway_config.yaml")


with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

def evaluate_gateway_policy(rule_score: float, semantic_score: float, pii_entities: list) -> tuple:
    r_w = config["thresholds"]["rule_weight"]
    s_w = config["thresholds"]["semantic_weight"]
    
    final_risk = (rule_score * r_w) + (semantic_score * s_w)
    
   
    if final_risk >= config["thresholds"]["block_threshold"] or rule_score >= 0.80:
        return round(final_risk, 2), "BLOCK", ["INJECTION_ATTEMPT"]
        
   
    if len(pii_entities) > 0:
        return round(final_risk, 2), "MASK", ["SENSITIVE_DATA_LEAKAGE"]
        
   
    return round(final_risk, 2), "ALLOW", ["ALL_CLEAR"]

import json
from datetime import datetime

def log_audit_request(input_id: str, decision: str, final_risk: float, latency_ms: float):
    """
    Gateway par aane wali har request ka ek auditable log record generate karne ke liye.
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "input_id": input_id,
        "decision": decision,
        "final_risk": final_risk,
        "latency_ms": latency_ms
    }
    
    # Console par real-time monitoring ke liye print karein
    print(f"[AUDIT LOG] {json.dumps(log_entry)}")
    
    # Optional: Aap isse kisi file mein bhi save karwa sakte hain append mode use karke
    try:
        with open("results/audit_history.log", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except:
        pass  # Agar folder ya permissions na hon to error skip karein
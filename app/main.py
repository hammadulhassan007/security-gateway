from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
import uuid
import sys
import os

# Yeh do lines Python ko batayengi ke 'app' folder ke andar ke saare folders ko sahi se dhoondhe
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Ab aapke saare imports bina kisi error ke chalenge
from utils.language import detect_language
from utils.logging import log_audit_request
from detectors.rule_detector import calc_rule_risk
from detectors.semantic_detector import semantic_detector
from pii.presidio_custom import process_pii
from policy.policy_engine import evaluate_gateway_policy

app = FastAPI(title="Robust Multilingual Security Gateway", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputPayload(BaseModel):
    msg: str

@app.get("/")
def home():
    return {"message": "Robust Multilingual Security Gateway is running live. Go to /docs to test."}

@app.post("/analyze")
async def analyze_input(payload: InputPayload):
    start_time = time.time()
    raw = payload.msg.strip()

    if not raw:
        raise HTTPException(status_code=400, detail="Empty input string not allowed")

    # 1. Pipeline Component: Language Recognition
    language = detect_language(raw)

    # 2. Pipeline Component: Hybrid Security Checks
    rule_score = calc_rule_risk(raw)
    semantic_score = semantic_detector.calc_semantic_risk(raw)

    # 3. Pipeline Component: Microsoft Presidio Data Masking
    pii_entities, safe_text = process_pii(raw)

    # 4. Pipeline Component: Policy Decision engine execution
    final_risk, decision, reason_codes = evaluate_gateway_policy(
        rule_score, semantic_score, pii_entities
    )

    # Latency Calculation
    latency_ms = round((time.time() - start_time) * 1000, 2)
    input_id = f"case_{uuid.uuid4().hex[:3]}"

    # 5. Pipeline Component: Audit Logging history update
    log_audit_request(input_id, decision, final_risk, latency_ms)

    # Standardized output JSON schema matching your university guidelines perfectly
    return {
        "input_id": input_id,
        "language": language,
        "rule_score": rule_score,
        "semantic_score": semantic_score,
        "pii_entities": pii_entities,
        "final_risk": final_risk,
        "decision": decision,
        "safe_text": safe_text if decision == "MASK" else (raw if decision == "ALLOW" else None),
        "reason_codes": reason_codes,
        "latency_ms": latency_ms
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
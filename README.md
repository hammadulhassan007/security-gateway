# 🛡️ InputGuard LLM: Security Gateway

**InputGuard LLM** is a lightweight, robust, and multilingual security gateway designed to protect Large Language Models (LLMs) from Prompt Injection Attacks (PIA) and unintended Personally Identifiable Information (PII) exfiltration. Operating as an isolated hybrid framework, it intercepts user prompts before they reach the model core.

---

## 👨‍🎓 Academic Details
* **Developer:** Hammad Ul Hassan
* **Registration Number:** FA24-BCS-076
* **University:** COMSATS University Islamabad, Wah Campus
* **Course:** AI Lab Final Project
* **Instructor:** Maam Tooba Tehreem

---

## ✨ Key Features
* **Hybrid Diagnostics Engine:** Combines explicit Rule-Based dictionary lookups with Semantic Character-Level TF-IDF Cosine-Similarity classification.
* **Contextual PII Masking:** Integrates a customized **Microsoft Presidio** engine. Automatically detects standard PII and localized Pakistani identifiers (e.g., CNIC, COMSATS Student IDs like `FA24-BCS-076`) with context-aware confidence boosting.
* **Multilingual Support:** Scans and processes Unicode properties to identify and filter malicious intent across English, Urdu, and Korean.
* **Dynamic Configuration:** Fully modular architecture with risk thresholds and weights managed centrally via `config/gateway_config.yaml`.
* **3-State Policy Convergence:** Routes prompts into three strict states: `ALLOW`, `MASK` (redacts PII before forwarding), or `BLOCK` (rejects adversarial inputs).

---

## 🏗️ System Architecture Pipeline

The text stream transitions through 5 distinct structural layers:
1. **Adaptive Ingestion & Sanitization Layer:** JSON validation and whitespace trimming.
2. **Deep Multilingual Script Layer:** Checks native Unicode distributions.
3. **Hybrid Multi-Vector Inspection Layer:** Parallel evaluation via Lexical Rules ($W = 0.40$) and Semantic TF-IDF Vectors ($W = 0.60$).
4. **Contextual PII Masking Layer:** Regex matching + Local context weight boost using Presidio.
5. **Distributed Policy Enforcement Layer:** Computes risk against YAML thresholds (Block Threshold $\ge 0.70$).

---

## 📊 Quantitative Evaluation & Metrics

The gateway was evaluated against a custom 155-row programmatic dataset comprising adversarial manipulations, localized roleplays, and PII leakage scenarios.

| Metric | Score | Interpretation |
| :--- | :--- | :--- |
| **Pipeline Accuracy** | `63.87%` | Overall classification correctness. |
| **Precision** | `1.00 (100%)` | Zero False Positives. Legitimate queries are NEVER blocked. |
| **Recall (Sensitivity)**| `0.3429 (34%)`| Conservative matching; strict threshold bypasses semantic obfuscation. |
| **F1-Score** | `0.5107` | Harmonic mean of Precision and Recall. |

---

## 📂 Project Structure

```text
security-gateway/
├── app/
│   ├── main.py                 # FastAPI Application Core
│   ├── detectors/              # Rule & Semantic Modules
│   ├── pii/                    # Custom Presidio Engine Config
│   ├── policy/                 # Final Output Logic Matrix
│   └── utils/                  # Logging and Language Parsing
├── config/
│   └── gateway_config.yaml     # Centralized thresholds & weights
├── data/
│   └── final_eval.csv          # 155-row Testing Dataset
├── results/
│   └── metrics_summary.json    # Automated Evaluation Outputs
├── run_evaluation.py           # Evaluation Script for Metrics
└── README.md

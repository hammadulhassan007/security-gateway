# Input Guard Pro - Secure Gateway for LLM  
** Lab Mid-Term **

**Student Name:** Hammad Ul Hassan FA24-BCS-076
**Instructor:** Tooba Tehreem  
**Email:** tooba@ciitwah.edu.pk  

## Project Overview
This is a security gateway project .. 

## Features
- Injection Detection with Scoring Mechanism
- Presidio with 3 Custom Recognizers (Phone, API Key, Internal ID)
- Policy: ALLOW / MASK / BLOCK
- Latency Measurement
- Configurable Threshold

## Installation Steps
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_lg
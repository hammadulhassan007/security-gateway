from langdetect import detect, DetectorFactory
import re

DetectorFactory.seed = 0

def detect_language(text: str) -> str:
    
    if re.search(r'[\u0600-\u06FF]', text):
        return "ur"
    try:
        return detect(text)
    except:
        return "en"

from presidio_analyzer import AnalyzerEngine, RecognizerResult, EntityRecognizer
from presidio_anonymizer import AnonymizerEngine
import re

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()


class LocalIdentityRecognizer(EntityRecognizer):
    def __init__(self):
        super().__init__(supported_entities=["CNIC", "STUDENT_ID", "API_KEY", "PHONE_NUMBER"])

    def analyze(self, text, entities=None, nlp_artifacts=None):
        results = []
        
    
        cnic_matches = re.finditer(r'\b\d{5}-\d{7}-\d{1}\b', text)
        for m in cnic_matches:
            results.append(RecognizerResult("CNIC", m.start(), m.end(), 0.85))
            
     
        id_matches = re.finditer(r'\b(CSC|FA|SP|CIIT)\d{2}-[A-Z]{3}-\d{3}\b', text, re.IGNORECASE)
        for m in id_matches:
            results.append(RecognizerResult("STUDENT_ID", m.start(), m.end(), 0.90))

     
        api_pattern = r'\b(sk-[a-zA-Z0-9]{20,}|pk_live_[a-zA-Z0-9]{20,}|AKIA[0-9A-Z]{16})\b'
        for m in re.finditer(api_pattern, text):
            results.append(RecognizerResult("API_KEY", m.start(), m.end(), 0.95))
            
       
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})'
        for m in re.finditer(phone_pattern, text):
            results.append(RecognizerResult("PHONE_NUMBER", m.start(), m.end(), 0.92))
            
        return results


analyzer.registry.add_recognizer(LocalIdentityRecognizer())

def process_pii(text: str):

    context_words = ["cnic", "identity", "phone", "student", "registration", "api", "key", "email"]
    boost = 0.10 if any(cw in text.lower() for cw in context_words) else 0.0

    raw_results = analyzer.analyze(text=text, language="en")
    processed_entities = []
    
    for res in raw_results:
      
        calibrated_score = min(res.score + boost, 1.0)
        
       
        if calibrated_score >= 0.60:
            res.score = calibrated_score
            processed_entities.append({
                "type": res.entity_type,
                "text": text[res.start:res.end],
                "score": round(res.score, 2)
            })

    
    masked_text = anonymizer.anonymize(text=text, analyzer_results=raw_results).text
    return processed_entities, masked_text

import spacy
from fuzzywuzzy import process

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# The vocabulary your system knows how to recognize
SYMPTOM_VOCAB = [
    "headache", "fever", "body ache", "fatigue", 
    "chest pain", "shortness of breath", "sweating", "nausea"
]

def extract_symptoms(user_text: str) -> list:
    doc = nlp(user_text.lower())
    
    # Extract base words (lemmas), ignoring punctuation and stop words (like 'the', 'is', 'a')
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    
    matched = []
    for token in tokens:
        # Compare the user's word against our known vocabulary using fuzzy matching
        result = process.extractOne(token, SYMPTOM_VOCAB, score_cutoff=75)
        if result:
            matched.append(result[0])
            
    # Return a unique list of matched symptoms
    return list(set(matched))
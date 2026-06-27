import json

def load_knowledge_base(path="data/annotated/symptom_data.json"):
    with open(path) as f:
        return json.load(f)

def find_conditions(symptoms: list, kb: list) -> list:
    results = []
    for entry in kb:
        # Find how many symptoms overlap between the user and the database entry
        overlap = set(symptoms) & set(entry["symptom_keywords"])
        
        if overlap:
            # Calculate a basic confidence score based on how many keywords matched
            score = len(overlap) / len(entry["symptom_keywords"])
            
            results.append({
                "conditions": entry["possible_conditions"],
                "severity": entry["severity"],
                "urgency": entry["urgency"],
                "recommendations": entry["recommendations"],
                "match_score": round(score, 2)
            })
            
    # Sort the results by highest match score and return the top 3
    return sorted(results, key=lambda x: x["match_score"], reverse=True)[:3]
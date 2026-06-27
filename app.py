from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

# Import your NLP engine extraction logic safely
try:
    from src.nlp_engine import extract_symptoms
except ImportError:
    # Reliable fallback if path routing defaults during migration
    def extract_symptoms(text):
        return [s.strip().lower() for s in text.split(",") if s.strip()]

app = Flask(__name__, template_folder="templates", static_folder="static")

# Safely load the dataset from the root folder
CSV_PATH = "symptoms.csv"
if os.path.exists(CSV_PATH):
    df = pd.read_csv(CSV_PATH)
    symptoms_db = df.to_dict(orient="records")
else:
    print(f"Error: {CSV_PATH} not found in the root directory!")
    symptoms_db = []

SEVERITY_RANK = {"Low": 1, "Medium": 2, "High": 3, "Unknown": 0}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json() or {}
    raw_text = data.get("symptoms", "").strip()

    if not raw_text:
        return jsonify({"error": "No symptoms provided"}), 400

    # Process the raw text using your project's native spaCy/NLP extractor!
    extracted_terms = extract_symptoms(raw_text)
    
    matched_results = []
    highest_severity = "Low"
    seen_conditions = set()

    # Compare extracted terms with your symptoms database rows
    for row in symptoms_db:
        db_symptom = str(row.get("symptom", "")).lower().strip()
        
        for term in extracted_terms:
            # Match keywords flexibly using substrings
            if db_symptom in term.lower() or term.lower() in db_symptom:
                condition = row.get("condition", "Unknown Condition")
                
                if condition not in seen_conditions:
                    seen_conditions.add(condition)
                    matched_results.append({
                        "condition": condition,
                        "recommendation": row.get("recommendation", "Consult a doctor."),
                        "medical_attention": row.get("medical_attention", "Monitor closely.")
                    })

                # Track highest overall safety severity metric
                current_severity = str(row.get("severity", "Low")).capitalize()
                if current_severity not in SEVERITY_RANK:
                    current_severity = "Low"
                if SEVERITY_RANK[current_severity] > SEVERITY_RANK[highest_severity]:
                    highest_severity = current_severity

    if not matched_results:
        return jsonify({
            "results": [{
                "condition": "No direct matches found",
                "recommendation": "Rest, hydrate, and track variations in what you feel.",
                "medical_attention": "Consult a healthcare professional for verification."
            }],
            "severity": "Unknown"
        })

    return jsonify({
        "results": matched_results,
        "severity": highest_severity
    })

if __name__ == "__main__":
    app.run(debug=True)
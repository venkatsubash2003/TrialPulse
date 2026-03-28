### Hey there
# nlp_scorer.py
import pandas as pd
def score_symptom(text: str) -> dict:
    text_lower = text.lower()

    if "tingling" in text_lower or "numbness" in text_lower:
        return {
            "grade": 2,
            "category": "Peripheral Neuropathy",
            "rationale": "Reported tingling/numbness indicates possible moderate neuropathy."
        }

    if "nausea" in text_lower or "vomiting" in text_lower:
        return {
            "grade": 2,
            "category": "Nausea",
            "rationale": "Symptoms suggest moderate gastrointestinal adverse event."
        }

    if "fatigue" in text_lower or "tired" in text_lower:
        return {
            "grade": 1,
            "category": "Fatigue",
            "rationale": "Reported fatigue appears mild based on text."
        }

    if "fever" in text_lower or "chills" in text_lower:
        return {
            "grade": 3,
            "category": "Fever / Infection Risk",
            "rationale": "Fever-related symptoms may require urgent follow-up."
        }

    return {
        "grade": 1,
        "category": "General Adverse Event",
        "rationale": "Low-confidence default classification based on limited symptom detail."
    }

def score_symptoms_in_df(df: pd.DataFrame, text_col: str = "symptom_text") -> pd.DataFrame:
    df = df.copy()
    results = df[text_col].apply(score_symptom)
    df["severity_grade"] = results.apply(lambda x: x["grade"])
    df["severity_category"] = results.apply(lambda x: x["category"])
    df["severity_rationale"] = results.apply(lambda x: x["rationale"])
    return df

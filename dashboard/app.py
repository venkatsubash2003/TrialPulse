##  fffsa
from flask import Flask, jsonify, render_template
import pandas as pd
import numpy as np
import random
import os

app = Flask(__name__)

REAL_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "demo_output.csv")

# ─────────────────────────────────────────────
# STUB INTERFACES — only used if CSV not found
# ─────────────────────────────────────────────

def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    STUB — Person B fills this in (IsolationForest).
    Input columns: heart_rate, systolic_bp, diastolic_bp, temperature, spo2
    Adds: anomaly_score (float), is_flagged (bool)
    """
    df["anomaly_score"] = np.random.uniform(0.0, 1.0, len(df)).round(2)
    df["is_flagged"] = df["anomaly_score"] > 0.75
    return df


def score_symptom(text: str) -> dict:
    """
    STUB — Person B fills this in (OpenAI + CTCAE grading).
    Input: symptom_text (str)
    Returns: severity_grade, severity_category, severity_rationale
    """
    if "tingling" in text or "fatigue" in text:
        return {"severity_grade": 2, "severity_category": "Peripheral Neuropathy",
                "severity_rationale": "Bilateral distal tingling with fatigue pattern consistent with Grade 2 sensory neuropathy. Requires clinical review within 48 hours per CTCAE v5.0 guidelines."}
    if "headache" in text or "dizziness" in text:
        return {"severity_grade": 2, "severity_category": "Headache / CNS",
                "severity_rationale": "Moderate headache with dizziness may indicate Grade 2 CNS adverse event. Blood pressure check and neurology consult recommended."}
    if "chest" in text or "shortness" in text:
        return {"severity_grade": 3, "severity_category": "Cardiac / Pulmonary",
                "severity_rationale": "Chest tightness with dyspnea warrants urgent Grade 3 assessment. Immediate ECG and oxygen saturation monitoring indicated."}
    if "vomiting" in text or "fever" in text:
        return {"severity_grade": 2, "severity_category": "Nausea / Pyrexia",
                "severity_rationale": "Vomiting with low-grade fever consistent with Grade 2 gastrointestinal toxicity. Antiemetic protocol and hydration assessment advised."}
    if "nausea" in text:
        return {"severity_grade": 1, "severity_category": "Nausea",
                "severity_rationale": "Mild post-prandial nausea consistent with Grade 1 GI adverse event. Monitor and reassess at next scheduled visit."}
    if "rash" in text:
        return {"severity_grade": 1, "severity_category": "Dermatologic",
                "severity_rationale": "Localised mild rash on extremities, Grade 1 dermatologic event. Topical treatment sufficient; no dose modification required."}
    return {"severity_grade": 1, "severity_category": "General / Unclassified",
            "severity_rationale": "Symptom pattern does not meet threshold for a specific CTCAE category. Routine monitoring recommended."}


def predict_dropout(df: pd.DataFrame) -> pd.DataFrame:
    """
    STUB — Person C fills this in (logistic regression).
    Input columns: missed_visits, response_delay_hours, wellbeing_score
    Adds: dropout_risk (float 0.0-1.0)
    """
    df["dropout_risk"] = np.random.uniform(0.0, 1.0, len(df)).round(2)
    return df


def compute_alert(row: pd.Series) -> dict:
    if row["is_flagged"] and row["dropout_risk"] > 0.7:
        return {
            "alert_level": "CRITICAL",
            "alert_message": (
                f"Multi-signal escalation — Vitals anomaly (score {row['anomaly_score']}), "
                f"Grade {row['severity_grade']} {row['severity_category']}, "
                f"and dropout risk at {int(row['dropout_risk']*100)}%. "
                "Recommend immediate coordinator contact."
            )
        }
    elif row["is_flagged"] or row["dropout_risk"] > 0.6:
        return {
            "alert_level": "WARNING",
            "alert_message": (
                f"Elevated risk — {'Vitals flagged. ' if row['is_flagged'] else ''}"
                f"Dropout risk at {int(row['dropout_risk']*100)}%. Schedule check-in call."
            )
        }
    else:
        return {
            "alert_level": "MONITOR",
            "alert_message": "Patient stable. Continue routine monitoring."
        }


# ─────────────────────────────────────────────
# DATA LOADER — real CSV first, synthetic fallback
# ─────────────────────────────────────────────

def load_data() -> pd.DataFrame:
    """
    Tries to load Person B's real output CSV.
    Falls back to synthetic data if file is missing.
    """
    if os.path.exists(REAL_DATA_PATH):
        print(f"[TrialPulse] Loading real data from {REAL_DATA_PATH}")
        df = pd.read_csv(REAL_DATA_PATH)

        # Ensure patient_id is zero-padded string e.g. P047
        if pd.api.types.is_integer_dtype(df["patient_id"]):
            df["patient_id"] = df["patient_id"].apply(lambda x: f"P{str(x).zfill(3)}")

        # Ensure is_flagged is boolean
        df["is_flagged"] = df["is_flagged"].astype(bool)

        return df

    # ── Synthetic fallback ──
    print("[TrialPulse] WARNING: Real data not found. Using synthetic data.")
    random.seed(42)
    np.random.seed(42)

    symptoms = [
        "mild fatigue and tingling in fingers",
        "severe headache and dizziness",
        "slight nausea after meals",
        "chest tightness and shortness of breath",
        "joint pain in knees",
        "no symptoms reported",
        "mild rash on arms",
        "vomiting and fever 38.5C",
    ]

    n = 200
    visit_dates = pd.date_range(end=pd.Timestamp.today(), periods=n, freq="6h")

    data = {
        "patient_id":           [f"P{str(i).zfill(3)}" for i in range(1, n + 1)],
        "visit_date":           [d.strftime("%Y-%m-%d %H:%M") for d in visit_dates],
        "heart_rate":           np.random.normal(75, 12, n).round(1),
        "systolic_bp":          np.random.normal(120, 15, n).round(1),
        "diastolic_bp":         np.random.normal(80, 10, n).round(1),
        "temperature":          np.random.normal(37.0, 0.5, n).round(1),
        "spo2":                 np.random.normal(97.5, 1.5, n).clip(90, 100).round(1),
        "symptom_text":         [random.choice(symptoms) for _ in range(n)],
        "missed_visits":        np.random.randint(0, 4, n),
        "response_delay_hours": np.random.uniform(0, 72, n).round(1),
        "wellbeing_score":      np.random.uniform(3.0, 10.0, n).round(1),
    }

    df = pd.DataFrame(data)
    df = detect_anomalies(df)
    df = predict_dropout(df)

    nlp_results = df["symptom_text"].apply(score_symptom)
    df["severity_grade"]     = nlp_results.apply(lambda x: x["severity_grade"])
    df["severity_category"]  = nlp_results.apply(lambda x: x["severity_category"])
    df["severity_rationale"] = nlp_results.apply(lambda x: x["severity_rationale"])

    alert_results = df.apply(compute_alert, axis=1)
    df["alert_level"]   = alert_results.apply(lambda x: x["alert_level"])
    df["alert_message"] = alert_results.apply(lambda x: x["alert_message"])

    # Force P047 demo patient
    df.loc[46, "symptom_text"]         = "mild fatigue and tingling in fingers"
    df.loc[46, "heart_rate"]           = 98.4
    df.loc[46, "systolic_bp"]          = 142.0
    df.loc[46, "diastolic_bp"]         = 95.0
    df.loc[46, "temperature"]          = 37.8
    df.loc[46, "spo2"]                 = 94.2
    df.loc[46, "missed_visits"]        = 2
    df.loc[46, "response_delay_hours"] = 58.0
    df.loc[46, "wellbeing_score"]      = 4.1
    df.loc[46, "anomaly_score"]        = 0.91
    df.loc[46, "is_flagged"]           = True
    df.loc[46, "dropout_risk"]         = 0.81
    df.loc[46, "severity_grade"]       = 2
    df.loc[46, "severity_category"]    = "Peripheral Neuropathy"
    df.loc[46, "severity_rationale"]   = "Bilateral distal tingling with fatigue pattern consistent with Grade 2 sensory neuropathy. Requires clinical review within 48 hours per CTCAE v5.0 guidelines."
    df.loc[46, "alert_level"]          = "CRITICAL"
    df.loc[46, "alert_message"]        = "Multi-signal escalation — Vitals anomaly (score 0.91), Grade 2 Peripheral Neuropathy, and dropout risk at 81%. Recommend immediate coordinator contact."

    return df


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("dashboard.html")


@app.route("/api/patients")
def patients():
    df = load_data()
    return jsonify(df.to_dict(orient="records"))


@app.route("/api/patient/<patient_id>")
def patient_detail(patient_id):
    df = load_data()
    row = df[df["patient_id"] == patient_id]
    if row.empty:
        return jsonify({"error": "Patient not found"}), 404
    return jsonify(row.iloc[0].to_dict())


@app.route("/api/stats")
def stats():
    df = load_data()
    return jsonify({
        "total_patients":   len(df),
        "critical":         int((df["alert_level"] == "CRITICAL").sum()),
        "warning":          int((df["alert_level"] == "WARNING").sum()),
        "monitor":          int((df["alert_level"] == "MONITOR").sum()),
        "avg_dropout_risk": round(float(df["dropout_risk"].mean()), 2),
        "data_source":      "real" if os.path.exists(REAL_DATA_PATH) else "synthetic"
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)

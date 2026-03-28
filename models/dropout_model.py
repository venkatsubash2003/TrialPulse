## Hey there
# dropout_model.py
import pandas as pd

def predict_dropout(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    risk = 0
    risk += (df["missed_visits"] >= 1).astype(int) * 0.35
    risk += (df["response_delay_hours"] > 24).astype(int) * 0.30
    risk += (df["wellbeing_score"] < 5).astype(int) * 0.20

    if "severity_grade" in df.columns:
        risk += (df["severity_grade"] >= 2).astype(int) * 0.15

    df["dropout_risk"] = risk.clip(0, 1)
    return df
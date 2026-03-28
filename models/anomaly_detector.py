## Anomaly detector.py
# anomaly_detector.py
# anomaly_detector.py
import pandas as pd

def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    required_cols = ["temperature", "heart_rate", "spo2", "systolic_bp", "diastolic_bp"]
    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns in anomaly detector: {missing}")

    df = df.copy()

    score = 0
    score += (df["temperature"] > 99.5).astype(int) * 0.25
    score += (df["heart_rate"] > 100).astype(int) * 0.20
    score += (df["spo2"] < 95).astype(int) * 0.30
    score += (df["systolic_bp"] < 95).astype(int) * 0.15
    score += (df["diastolic_bp"] < 60).astype(int) * 0.10

    df["anomaly_score"] = score.clip(0, 1)
    df["is_flagged"] = df["anomaly_score"] >= 0.4
    return df
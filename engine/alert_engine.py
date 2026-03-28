#h ye
# alert_engine.py
import pandas as pd

def generate_alerts(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    levels = []
    messages = []

    for _, row in df.iterrows():
        if row["dropout_risk"] >= 0.75 or (row["severity_grade"] >= 3) or (row["anomaly_score"] >= 0.7):
            level = "CRITICAL"
        elif row["dropout_risk"] >= 0.45 or row["severity_grade"] >= 2 or row["anomaly_score"] >= 0.4:
            level = "WARNING"
        else:
            level = "MONITOR"

        if level == "CRITICAL":
            msg = f"Patient {row['patient_id']} — multi-signal escalation. Immediate follow-up required."
        elif level == "WARNING":
            msg = f"Patient {row['patient_id']} — moderate risk detected. Coordinator review recommended."
        else:
            msg = f"Patient {row['patient_id']} — currently stable. Continue monitoring."

        levels.append(level)
        messages.append(msg)

    df["alert_level"] = levels
    df["alert_message"] = messages
    return df
#h ye
# alert_engine.py
import pandas as pd

def generate_alerts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Input: dataframe containing anomaly_score, is_flagged, symptom severity, dropout_risk
    Output: same dataframe with:
      - alert_level
      - alert_message
    """
    pass
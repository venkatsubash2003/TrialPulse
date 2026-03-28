import pandas as pd

from models.anomaly_detector import detect_anomalies
from models.nlp_scorer import score_symptoms_in_df
from models.dropout_model import predict_dropout
from engine.alert_engine import generate_alerts


def run_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    df = detect_anomalies(df)
    df = score_symptoms_in_df(df)
    df = predict_dropout(df)
    df = generate_alerts(df)

    return df
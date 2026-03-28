# Person C owns this file
import pandas as pd
import pandas as pd


def load_data() -> pd.DataFrame:
    data = [
        {
            "patient_id": 12,
            "visit_date": "2026-03-28",
            "heart_rate": 76,
            "systolic_bp": 118,
            "diastolic_bp": 76,
            "temperature": 98.4,
            "spo2": 98,
            "symptom_text": "Mild tiredness after a long day, otherwise feeling okay.",
            "missed_visits": 0,
            "response_delay_hours": 2,
            "wellbeing_score": 8,
        },
        {
            "patient_id": 23,
            "visit_date": "2026-03-28",
            "heart_rate": 96,
            "systolic_bp": 108,
            "diastolic_bp": 70,
            "temperature": 99.2,
            "spo2": 96,
            "symptom_text": "Feeling more tired than usual with some nausea since yesterday.",
            "missed_visits": 1,
            "response_delay_hours": 14,
            "wellbeing_score": 6,
        },
        {
            "patient_id": 31,
            "visit_date": "2026-03-28",
            "heart_rate": 118,
            "systolic_bp": 90,
            "diastolic_bp": 58,
            "temperature": 101.4,
            "spo2": 92,
            "symptom_text": "Fever with chills, vomiting, weakness, and shortness of breath.",
            "missed_visits": 2,
            "response_delay_hours": 32,
            "wellbeing_score": 3,
        },
        {
            "patient_id": 47,
            "visit_date": "2026-03-28",
            "heart_rate": 109,
            "systolic_bp": 94,
            "diastolic_bp": 60,
            "temperature": 100.3,
            "spo2": 94,
            "symptom_text": "Mild fatigue and tingling in fingers for the past two days.",
            "missed_visits": 2,
            "response_delay_hours": 28,
            "wellbeing_score": 4,
        },
        {
            "patient_id": 55,
            "visit_date": "2026-03-28",
            "heart_rate": 88,
            "systolic_bp": 122,
            "diastolic_bp": 80,
            "temperature": 98.9,
            "spo2": 97,
            "symptom_text": "Occasional headache but overall manageable and able to continue daily tasks.",
            "missed_visits": 0,
            "response_delay_hours": 6,
            "wellbeing_score": 7,
        },
    ]

    return pd.DataFrame(data)
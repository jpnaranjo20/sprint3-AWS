import psycopg2
from psycopg2.extensions import connection

DATABASE_URL = "postgresql://anyone_ai:anyone_ai@postgres/ml_app"


def get_db() -> connection:
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def create_table():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            gender VARCHAR(10),
            age INT,
            hypertension INT,
            heart_disease INT,
            smoking_history VARCHAR(20),
            bmi FLOAT,
            HbA1c_level FLOAT,
            blood_glucose_level INT,
            prediction FLOAT
        );
    """
    )
    conn.commit()
    cur.close()
    conn.close()


def insert_prediction(
    gender: str,
    age: int,
    hypertension: int,
    heart_disease: int,
    smoking_history: str,
    bmi: float,
    HbA1c_level: float,
    blood_glucose_level: int,
    prediction: float,
):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO predictions (gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level, prediction)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """,
        (
            gender,
            age,
            hypertension,
            heart_disease,
            smoking_history,
            bmi,
            HbA1c_level,
            blood_glucose_level,
            prediction,
        ),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_predictions():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM predictions")
    predictions = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "id": p[0],
            "gender": p[1],
            "age": p[2],
            "hypertension": p[3],
            "heart_disease": p[4],
            "smoking_history": p[5],
            "bmi": p[6],
            "HbA1c_level": p[7],
            "blood_glucose_level": p[8],
            "prediction": p[9],
        }
        for p in predictions
    ]

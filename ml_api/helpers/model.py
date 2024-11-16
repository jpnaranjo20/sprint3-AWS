import redis, time, json
from uuid import uuid4


db = redis.Redis(host="redis", port=6379, db=0)


def predict(
    gender: str,
    age: int,
    hypertension: int,
    heart_disease: int,
    smoking_history: str,
    bmi: float,
    HbA1c_level: float,
    blood_glucose_level: int,
) -> float:

    job_id = str(uuid4())
    job_data = {
        "id": job_id,
        "gender": gender,
        "age": age,
        "hypertension": hypertension,
        "heart_disease": heart_disease,
        "smoking_history": smoking_history,
        "bmi": bmi,
        "HbA1c_level": HbA1c_level,
        "blood_glucose_level": blood_glucose_level,
    }

    db.lpush("service_queue", json.dumps(job_data))

    # Loop until we received the response from our ML model
    while True:
        output = db.get(job_id)

        # Check if the text was correctly processed by our ML model
        if output is not None:
            output = json.loads(output.decode("utf-8"))  # type: ignore
            prediction = output["prediction"]

            db.delete(job_id)
            break

        # Sleep some time waiting for model results
        time.sleep(0.05)

    return prediction

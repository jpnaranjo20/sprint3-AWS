import json
import time
from uuid import uuid4

import redis

from .. import settings

# Connect to Redis and assign to variable `db``
try: 
    db = redis.StrictRedis(
        host=settings.REDIS_IP,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB_ID,
        decode_responses=True
    )
    print('Successfully connected to Redis!')
except Exception as e:
    print('There was a problem connecting to Redis: {e}')


async def model_predict(image_name):
    print(f"Processing image {image_name}...")
    """
    Receives an image name and queues the job into Redis.
    Will loop until getting the answer from our ML service.

    Parameters
    ----------
    image_name : str
        Name for the image uploaded by the user.

    Returns
    -------
    prediction, score : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    prediction = None
    score = None
    
    #generate a unique ID for the job, using uuid4
    #uuid4 is used to ensure that the generated id is secure. 
    #a secure UUID is one that is generated using synchronization methods that ensure that no two processes can get the same UUID. 
    #that no two processes can get the same UUID. 
    job_id = str(uuid4())

    #create a job object with the job_id and the image name
    job_data = {
        "id": job_id,
        "image_name": image_name
        }

    # I send the job to the service of the model, for that I insert it
    # in the redis queue configured as an environment variable in settings
    db.lpush(settings.REDIS_QUEUE,json.dumps(job_data))

    # Loop until we received the response from our ML model
    while True:
        # Attempt to get model predictions using job_id
        # Hint: Investigate how can we get a value using a key from Redis
        output = db.get(job_id)

        # Check if the text was correctly processed by our ML model
        # Don't modify the code below, it should work as expected
        if output is not None:
            output = output.encode("utf-8")
            output = json.loads(output.decode("utf-8"))
            prediction = output["prediction"]
            score = output["score"]

            db.delete(job_id)
            break

        # Sleep some time waiting for model results
        time.sleep(settings.API_SLEEP)

    return prediction, score

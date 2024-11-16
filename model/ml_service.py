import json
import os
import time

import numpy as np
import redis
import settings
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image

# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
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

# Load your ML model and assign to variable `model`
# See https://drive.google.com/file/d/1ADuBSE4z2ZVIdn66YDSwxKv-58U7WEOn/view?usp=sharing
# for more information about how to use this model.
model = ResNet50(weights='imagenet')


def predict(image_name):
    """
    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.

    Parameters
    ----------
    image_name : str
        Image filename.

    Returns
    -------
    class_name, pred_probability : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    class_name = None
    pred_probability = None
    # Implement the code to predict the class of the image_name

    # Load image
    im_path = os.path.join(settings.UPLOAD_FOLDER, image_name)
    img = image.load_img(im_path, target_size=(224,224))
    # Apply preprocessing (convert to numpy array, match model input dimensions (including batch) and use the resnet50 preprocessing)
    im_array = image.img_to_array(img)
    im_array = np.expand_dims(im_array, axis=0)
    im_array = preprocess_input(im_array)
    # Get predictions using model methods and decode predictions using resnet50 decode_predictions
    preds = model.predict(im_array)
    decoded_preds = decode_predictions(preds, top=1)[0]
    class_name = decoded_preds[0][1]

    # Convert probabilities to float and round it
    pred_probability = round(float(decoded_preds[0][2]), 4)
    
    return class_name, pred_probability


def classify_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.

    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.
    """
    while True:
        # Inside this loop you should add the code to:
        #   1. Take a new job from Redis
        #   2. Run your ML model on the given data
        #   3. Store model prediction in a dict with the following shape:
        #      {
        #         "prediction": str,
        #         "score": float,
        #      }
        #   4. Store the results on Redis using the original job ID as the key
        #      so the API can match the results it gets to the original job
        #      sent
        # Hint: You should be able to successfully implement the communication
        #       code with Redis making use of functions `brpop()` and `set()`.
        # 
        # Take a new job from Redis

        # brpop is a Redis command that pops a value from the tail of a list, blocking the connection
        # until a value is available. 
        # pop from head of the queue (right of list)
        # the b in brpop indicates this is a blocking call (waits until an item becomes available).
        job = db.brpop(settings.REDIS_QUEUE)

        print(f'Job received:{job}')

        #adicional 
        if job is None:
            time.sleep(settings.SERVER_SLEEP)
            continue

        _, job_data = job

        print(f'Job data PREVIO:{job_data}')

        job_random=job_data.encode("utf-8")

        job_data = json.loads(job_random.decode("utf-8"))

        print(f'Job data FINAL:{job_data}')

        # Important! Get and keep the original job ID
        job_id = job_data.get("id")

        # Run the loaded ml model (use the predict() function)
        class_name, pred_probability = predict(job_data.get("image_name"))

        # Prepare a new JSON with the results
        output = {"prediction": class_name, "score": pred_probability}

        # Store the job results on Redis using the original
        # job ID as the key
        db.set(job_id,json.dumps(output))
        # Sleep for a bit
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()

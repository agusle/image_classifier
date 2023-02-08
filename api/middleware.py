import time
import settings
import redis
import uuid
import json

# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
    host=settings.REDIS_IP, port=settings.REDIS_PORT, db=settings.REDIS_DB_ID
)


def model_predict(image_name):
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
    job_id = str(uuid.uuid4()) 

    job_data = {
        "id": job_id,
        "image_name": image_name,
    }

    # Send the job to the model service using Redis
    job_data_str = json.dumps(job_data)
    db.rpush(settings.REDIS_QUEUE, job_data_str)

    # Loop until we received the response from our ML model
    while True:
        # Attempt to get model predictions using job_id
        # Hint: Investigate how can we get a value using a key from Redis
        output = None
        if db.exists(job_id):
            # Get job of redis queue
            output = json.loads(db.get(job_id))
            # Don't forget to delete the job from Redis after we get the results!
            # Then exit the loop
            db.delete(job_id)
            break
        # Sleep some time waiting for model results
        time.sleep(settings.API_SLEEP)
    # Load job as a dict
    return tuple([output["prediction"], output["score"]])

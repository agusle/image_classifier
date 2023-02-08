import time
import redis
import settings
from tensorflow.keras.applications import resnet50
from tensorflow.keras.preprocessing import image
import os
import numpy as np
import json


# Connect to Redis and assign to variable `db``
db = redis.Redis(
    host=settings.REDIS_IP, port=settings.REDIS_PORT, db=settings.REDIS_DB_ID
)
# Load your ML model and assign to variable `model`
model = resnet50.ResNet50(include_top=True, weights="imagenet")


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
    # create image path from concatenation
    image_path = os.path.join(settings.UPLOAD_FOLDER, image_name)
    # load image and resize
    image_file = image.load_img(image_path, target_size=(224, 224))
    # preprocess image
    image_prepro = image.img_to_array(image_file)
    image_prepro = np.expand_dims(image_prepro, axis=0)
    image_prepro = resnet50.preprocess_input(image_prepro)

    # predictions with resnet50
    pred = model.predict(image_prepro)
    result = resnet50.decode_predictions(pred, top=1)[0][0]

    return tuple([str(result[1]), round(float(result[2]), 4)])


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
        #   1. Take a new job from Redis
        queue_name, msg = db.brpop(settings.REDIS_QUEUE)
        if msg:
            msg = json.loads(msg)
            #   2. Run your ML model on the given data
            pred_class, pred_score = predict(msg["image_name"])
            #   3. Store model prediction in a dict
            output_msg = {
                "prediction": pred_class,
                "score": pred_score,
            }
            #   4. Store the results on Redis using the original job ID as the key
            #      so the API can match the results it gets to the original job sent
            db.set(msg["id"], json.dumps(output_msg))

        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    print("Launching ML service...")
    classify_process()

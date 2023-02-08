import utils
import os
import settings
from middleware import model_predict
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
)
from datetime import datetime


router = Blueprint("app_router", __name__, template_folder="templates")


@router.route("/", methods=["GET"])
def index():
    """
    Index endpoint, renders our HTML code.
    """
    return render_template("index.html")


@router.route("/", methods=["POST"])
def upload_image():
    """
    Function used in our frontend so we can upload and show an image.
    When it receives an image from the UI, it also calls our ML model to
    get and display the predictions.
    """
    # No file received, show basic UI
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)

    # File received but no filename is provided, show basic UI
    file = request.files["file"]
    if file.filename == "":
        flash("No image selected for uploading")
        return redirect(request.url)

    # File received and it's an image, we must show it and get predictions
    if file and utils.allowed_file(file.filename):

        #   1. Get an unique file name
        unique_filename = utils.get_file_hash(file)

        #   2. Store the image to disk using the new name
        image_path = os.path.join(settings.UPLOAD_FOLDER, unique_filename)

        # Check the file already exist
        if not os.path.exists(image_path):
            file.save(image_path)

        context = {
            "prediction": None,
            "score": None,
            "filename": None,
            "time": None,
        }

        #   3. Send the file to be processed by the `model` service
        before = datetime.now()
        pred_result = model_predict(unique_filename)
        after = datetime.now()
        time = after - before
        print(f"model_predict_root_route took {time} seconds")

        #   4. Update `context` dict with the corresponding values
        context.update(
            {
                "prediction": pred_result[0],
                "score": pred_result[1],
                "filename": unique_filename,
                "time": time,
            }
        )

        # Update `render_template()` parameters as needed

        return render_template(
            "index.html", filename=unique_filename, context=context
        )
    # File received and but it isn't an image
    else:
        flash("Allowed image types are -> png, jpg, jpeg, gif")
        return redirect(request.url)


@router.route("/display/<filename>")
def display_image(filename):
    """
    Display uploaded image in our UI.
    """
    return redirect(
        url_for("static", filename="uploads/" + filename), code=301
    )


@router.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint used to get predictions without need to access the UI.

    Parameters
    ----------
    file : str
        Input image we want to get predictions from.

    Returns
    -------
    flask.Response
        JSON response from our API having the following format:
            {
                "success": bool,
                "prediction": str,
                "score": float,
            }

        - "success" will be True if the input file is valid and we get a
          prediction from our ML model.
        - "prediction" model predicted class as string.
        - "score" model confidence score for the predicted class as float.
    """
    #   1. Check a file was sent and that file is an image
    if "file" in request.files:
        file = request.files["file"]

        if file and utils.allowed_file(file.filename):
            unique_filename = utils.get_file_hash(file)
            image_path = os.path.join(settings.UPLOAD_FOLDER, unique_filename)

            #   2. Store the image to disk if it does not exist
            if not os.path.exists(image_path):
                file.save(image_path)

            #   3. Send the file to be processed by the `model` service
            before = datetime.now()
            pred_result = model_predict(unique_filename)
            after = datetime.now()
            print(f"model_predict_predict_route took {after-before} seconds")

            #   4. Update and return `rpse` dict with the corresponding values
            # If user sends an invalid request (e.g. no file provided) this endpoint
            # should return `rpse` dict with default values HTTP 400 Bad Request code
            rpse = {
                "success": True,
                "prediction": pred_result[0],
                "score": pred_result[1],
            }
            return jsonify(rpse), 200

    rpse = {"success": False, "prediction": None, "score": None}
    return jsonify(rpse), 400


@router.route("/feedback", methods=["GET", "POST"])
def feedback():
    """
    Store feedback from users about wrong predictions on a text file.

    Parameters
    ----------
    report : request.form
        Feedback given by the user with the following JSON format:
            {
                "filename": str,
                "prediction": str,
                "score": float
            }

        - "filename" corresponds to the image used stored in the uploads
          folder.
        - "prediction" is the model predicted class as string reported as
          incorrect.
        - "score" model confidence score for the predicted class as float.
    """
    # Get reported predictions from `report` key
    report = request.form.get("report")
    # Store the reported data to a file on the corresponding path
    # already provided in settings.py module
    feedback_path = settings.FEEDBACK_FILEPATH
    # create file
    with open(feedback_path, "a+") as f:
        f.write(f"{report}\n")
        flash("Thanks for your feedback")

    return render_template("index.html")

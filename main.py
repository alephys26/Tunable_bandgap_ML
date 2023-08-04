from flask import Flask, render_template, request
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import base64
import zlib

app = Flask(__name__)

# Load your Keras model
model_min1 = load_model("model_min1.h5")
model_max1 = load_model("model_max1.h5")
model_min2 = load_model("model_min2.h5")
model_max2 = load_model("model_max2.h5")

# Define a route for the home page
@app.route("/", methods=["GET", "POST"])
def index():
    max1, min1, max2, min2 = 0, 0, 0, 0
    image_data = None
    if request.method == "POST":
        # Get the user input from the form
        length = float(request.form["len"])
        micro = request.form["micro"]
        flux = float(request.form["flux"])
        beta = float(request.form["beta"])
        alpha = float(request.form["alpha"])
        jm = float(request.form["jm"])
        input_data = preprocess_user_input(length, alpha, beta, flux, jm, micro)
        # Make predictions using your Keras model
        min1 = postprocess(model_min1.predict(input_data), "min1")
        max1 = postprocess(model_max1.predict(input_data), "max1")
        min2 = postprocess(model_min2.predict(input_data), "min2")
        max2 = postprocess(model_max2.predict(input_data), "max2")
        image_data = genImage(micro)
    return render_template(
        "home.html", min1=min1, max1=max1, min2=min2, max2=max2, image_data=image_data
    )


def preprocess_user_input(length, alpha, beta, flux, ja, ms):
    # Implement any preprocessing needed for your model input
    # Convert the user input to a suitable format for the model
    dt = {
        "length": {"mean": 0.050655321653004556, "std": 0.028533322704474576},
        "alpha": {"mean": 24.83735219840415, "std": 14.42185037044692},
        "beta": {"mean": 25.025481487579157, "std": 14.281687087068281},
        "flux": {"mean": -0.010348265596617931, "std": 2.8837338353651276},
        "ja": {"mean": 501.7442993509522, "std": 286.95913808062977},
        "ms": {"mean": 10239.55475, "std": 1323.132471899436},
    }
    # MS Preprocessing
    msi = [ms[i * 10 : i * 10 + 9] for i in range(20)]
    msi = [int(i, base=2) for i in msi]
    micro = 0
    for i in msi:
        micro += i

    features = [length, alpha, beta, flux, ja, micro]
    for i, c in enumerate(["length", "alpha", "beta", "flux", "ja", "ms"]):
        features[i] = (features[i] - dt[c]["mean"]) / dt[c]["std"]
    return np.array([features])


def postprocess(value, type):
    val = value[0][0]
    # dt = {
    #     "max1": {"mean": 15398.844113319825, "std": 42905.60053540335},
    #     "min1": {"mean": 14697.45426318213, "std": 41342.5015013504},
    #     "max2": {"mean": 30881.422584397893, "std": 86044.94420467704},
    #     "min2": {"mean": 29318.121128388106, "std": 82462.01857216492},
    # }
    # val = val * dt[type]["std"] + dt[type]["mean"]
    return val


def genImage(st):
    # Create a blank canvas as a NumPy array
    width, height = 200, 50
    canvas = np.zeros((height, width, 3), dtype=np.uint8)

    for i, s in enumerate(st):
        if int(s) == 1:
            canvas[:, i] = [255, 0, 0]  # Draw a red rectangle

    # Convert the NumPy array to bytes
    image_bytes = canvas.tobytes()

    # Convert the bytes to a base64 encoded string
    img_str = base64.b64encode(image_bytes).decode("utf-8")

    return img_str


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)

# Load models
maison_model = joblib.load("models/maison_random_forest_model.pkl")
appart_model = joblib.load("models/apt_random_forest_model.pkl")

# Get feature names
features_maison = list(maison_model.feature_names_in_)
features_appart = list(appart_model.feature_names_in_)

# Season mapping for reference
SEASON_MAPPING = {"winter": 0, "spring": 1, "summer": 2, "autumn": 3}


@app.route("/", methods=["GET", "POST"])
def index():

    prediction = None
    form_type = None
    feature_list = []

    if request.method == "POST":

        form_type = request.form.get("form_type")

        if form_type == "maison":
            model = maison_model
            feature_list = features_maison

        elif form_type == "appartement":
            model = appart_model
            feature_list = features_appart

        # Build feature array dynamically
        values = []
        for feature in feature_list:
            val = float(request.form.get(feature, 0))
            values.append(val)

        features_array = np.array([values])

        prediction = model.predict(features_array)[0]

    return render_template(
        "index.html",
        prediction=prediction,
        form_type=form_type,
        features_maison=features_maison,
        features_appart=features_appart
    )


if __name__ == "__main__":
    app.run(debug=True)
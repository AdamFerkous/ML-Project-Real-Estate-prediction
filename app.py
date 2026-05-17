from flask import Flask, render_template, request
import numpy as np
import joblib
import os

app = Flask(__name__)

# Load models for both departments
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODELS = {}
DEPARTMENTS = ["75", "77"]

for dept in DEPARTMENTS:
    try:
        maison_path = os.path.join(BASE_DIR, f"models/maison_rf_model_{dept}.pkl")
        appart_path = os.path.join(BASE_DIR, f"models/appartement_rf_model_{dept}.pkl")
        
        MODELS[dept] = {
            "maison": joblib.load(maison_path),
            "appartement": joblib.load(appart_path)
        }
        print(f"✓ Loaded models for department {dept}")
    except Exception as e:
        print(f"❌ Failed to load models for department {dept}: {e}")

# Get feature names from first available model
features_maison = None
features_appart = None
for dept in DEPARTMENTS:
    if dept in MODELS:
        if features_maison is None:
            features_maison = list(MODELS[dept]["maison"].feature_names_in_)
        if features_appart is None:
            features_appart = list(MODELS[dept]["appartement"].feature_names_in_)

# Season mapping for reference
SEASON_MAPPING = {"winter": 0, "spring": 1, "summer": 2, "autumn": 3}

# Custom filter for price formatting
@app.template_filter('format_price')
def format_price_filter(value):
    """Format price with spaces as thousand separators"""
    if value is None:
        return ""
    return f"{int(value):,}".replace(",", " ")


@app.route("/", methods=["GET", "POST"])
def index():

    prediction = None
    form_type = None
    selected_dept = None
    feature_list = []
    error_message = None

    if request.method == "POST":

        form_type = request.form.get("form_type")
        selected_dept = request.form.get("department", "75")

        # Validate department
        if selected_dept not in DEPARTMENTS or selected_dept not in MODELS:
            error_message = f"Department {selected_dept} not available"
        else:
            try:
                if form_type == "maison":
                    model = MODELS[selected_dept]["maison"]
                    feature_list = features_maison

                elif form_type == "appartement":
                    model = MODELS[selected_dept]["appartement"]
                    feature_list = features_appart

                else:
                    error_message = "Invalid property type"

                # Build feature array dynamically if no error
                if not error_message:
                    values = []
                    for feature in feature_list:
                        val = float(request.form.get(feature, 0))
                        values.append(val)

                    features_array = np.array([values])

                    prediction = model.predict(features_array)[0]
            except Exception as e:
                error_message = f"Error during prediction: {str(e)}"

    return render_template(
        "index.html",
        prediction=prediction,
        form_type=form_type,
        selected_dept=selected_dept,
        departments=DEPARTMENTS,
        features_maison=features_maison,
        features_appart=features_appart,
        error_message=error_message
    )


if __name__ == "__main__":
    app.run(debug=True)
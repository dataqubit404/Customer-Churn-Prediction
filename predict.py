import pandas as pd
import joblib
import os

# ==============================
# Load Model and Feature Columns
# ==============================

ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(ROOT, "models", "best_model.pkl")
FEATURE_PATH = os.path.join(ROOT, "models", "feature_columns.pkl")

model = joblib.load(MODEL_PATH)
feature_columns = joblib.load(FEATURE_PATH)


# ==============================
# Prediction Function
# ==============================

def predict_churn(input_dict):

    # Convert input to DataFrame
    input_df = pd.DataFrame([input_dict])

    # One-hot encode categorical features
    input_df = pd.get_dummies(input_df)

    # Add missing columns from training
    for col in feature_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    # Ensure same column order
    input_df = input_df[feature_columns]

    # Make prediction
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    # Detect correct churn class
    classes = model.classes_

    if "Yes" in classes:
        churn_index = list(classes).index("Yes")
    else:
        churn_index = list(classes).index(1)

    churn_probability = probabilities[churn_index]

    return prediction, churn_probability
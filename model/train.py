# model/train.py
# Final Professional Version - Phase 6 Complete

import os
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

# -------------------------------
# 1️⃣ Get project root
# -------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df_path = os.path.join(ROOT, "data", "telco_churn_clean.csv")

# -------------------------------
# 2️⃣ Load dataset
# -------------------------------
df = pd.read_csv(df_path)
print("Dataset loaded successfully!")
print("Shape:", df.shape)

# -------------------------------
# 3️⃣ Encode Target Variable
# -------------------------------
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

# -------------------------------
# 4️⃣ Separate Features
# -------------------------------
categorical_features = ["gender", "Partner", "Dependents",
                        "PhoneService", "MultipleLines", "InternetService",
                        "OnlineSecurity", "OnlineBackup", "DeviceProtection",
                        "TechSupport", "StreamingTV", "StreamingMovies",
                        "Contract", "PaperlessBilling", "PaymentMethod"]

numerical_features = ["tenure", "MonthlyCharges", "TotalCharges"]

# -------------------------------
# 5️⃣ Label Encoding (Binary)
# -------------------------------
le = LabelEncoder()
binary_cols = ["gender", "Partner", "Dependents", "PhoneService", "PaperlessBilling"]

for col in binary_cols:
    df[col] = le.fit_transform(df[col])

# -------------------------------
# 6️⃣ One-Hot Encoding
# -------------------------------
multi_cols = ["MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
              "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
              "Contract", "PaymentMethod"]

df = pd.get_dummies(df, columns=multi_cols, drop_first=True)

# -------------------------------
# 7️⃣ Scale Numerical Features
# -------------------------------

# -------------------------------
# 8️⃣ Split Features & Target
# -------------------------------
X = df.drop(["customerID", "Churn"], axis=1)
y = df["Churn"]

print("\nChurn distribution:")
print(y.value_counts())
print("\nChurn percentage:")
print(y.value_counts(normalize=True))

# -------------------------------
# 9️⃣ Train-Test Split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("\nTrain-test split done")
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)

# -------------------------------
# 🔟 Initialize Tuned Models
# -------------------------------
models = {
    "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
    "RandomForest": RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        random_state=42
    ),
    "XGBoost": XGBClassifier(
        n_estimators=400,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric='logloss'
    )
}

# -------------------------------
# 1️⃣1️⃣ Cross Validation
# -------------------------------
print("\nCross Validation Scores (ROC-AUC):")
for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc')
    print(f"{name}: {round(scores.mean(), 4)}")

# -------------------------------
# 1️⃣2️⃣ Train & Evaluate
# -------------------------------
results = {}

for name, model in models.items():
    print(f"\nTraining {name}...")
    model.fit(X_train, y_train)

    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_proba > 0.35).astype(int)  # Threshold adjustment

    results[name] = {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "ROC-AUC": roc_auc_score(y_test, y_proba),
        "ConfusionMatrix": confusion_matrix(y_test, y_pred)
    }

    print(f"\n=== {name} ===")
    print("Accuracy:", round(results[name]["Accuracy"], 4))
    print("Precision:", round(results[name]["Precision"], 4))
    print("Recall:", round(results[name]["Recall"], 4))
    print("ROC-AUC:", round(results[name]["ROC-AUC"], 4))
    print("Confusion Matrix:\n", results[name]["ConfusionMatrix"])
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

# -------------------------------
# 1️⃣3️⃣ Select Best Model Automatically
# -------------------------------
best_model_name = max(results, key=lambda x: results[x]["ROC-AUC"])
best_model = models[best_model_name]

print(f"\n🏆 Best Model Based on ROC-AUC: {best_model_name}")

# -------------------------------
# 1️⃣4️⃣ Save Best Model
# -------------------------------
models_folder = os.path.join(ROOT, "models")
os.makedirs(models_folder, exist_ok=True)

joblib.dump(best_model, os.path.join(models_folder, "best_model.pkl"))
joblib.dump(X_train.columns.tolist(), os.path.join(models_folder, "feature_columns.pkl"))

print("Best model saved successfully!")

# -------------------------------
# 1️⃣5️⃣ Feature Importance (XGBoost Only)
# -------------------------------
if best_model_name == "XGBoost":
    importance = best_model.feature_importances_
    features = X_train.columns

    plt.figure(figsize=(8, 6))
    plt.barh(features, importance)
    plt.title("Feature Importance - XGBoost")
    plt.tight_layout()
    plt.show()
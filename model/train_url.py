import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Project folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dataset
dataset_path = os.path.join(
    BASE_DIR,
    "dataset",
    "phishing_url_dataset",
    "web-page-phishing.csv"
)

# Read dataset
df = pd.read_csv(dataset_path)

# Features
X = df.drop("phishing", axis=1)

# Target
y = df["phishing"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train Model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Accuracy
prediction = model.predict(X_test)

accuracy = accuracy_score(y_test, prediction)

print("Accuracy :", accuracy)

# Save Model
joblib.dump(model, os.path.join(BASE_DIR, "model", "url_model.pkl"))

print("URL Model Saved Successfully!")
import pandas as pd
import os
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Project folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dataset_folder = os.path.join(BASE_DIR, "dataset", "phishing_email_dataset")

all_data = []

# Read all CSV files
for file in os.listdir(dataset_folder):

    if file.endswith(".csv"):

        path = os.path.join(dataset_folder, file)

        df = pd.read_csv(path, encoding="latin1")

        # Different datasets have different text columns
        if "body" in df.columns:
            text = df["body"]

        elif "text_combined" in df.columns:
            text = df["text_combined"]

        else:
            continue

        label = df["label"]

        temp = pd.DataFrame({
            "text": text,
            "label": label
        })

        all_data.append(temp)

# Merge all datasets
data = pd.concat(all_data, ignore_index=True)

# Remove empty rows
data.dropna(inplace=True)

print("Total Emails :", len(data))

# Convert labels to numbers
data["label"] = data["label"].replace({
    "phishing": 1,
    "spam": 1,
    "Fraud": 1,
    "fraud": 1,
    "legitimate": 0,
    "ham": 0
})

data["label"] = data["label"].astype(int)

# Features
X = data["text"]

# Labels
y = data["label"]

# Convert text into numbers
vectorizer = TfidfVectorizer(stop_words="english")

X = vectorizer.fit_transform(X)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train Model
model = MultinomialNB()

model.fit(X_train, y_train)

# Accuracy
prediction = model.predict(X_test)

accuracy = accuracy_score(y_test, prediction)

print("Accuracy :", accuracy)

# Save Model
joblib.dump(model, os.path.join(BASE_DIR, "model", "email_model.pkl"))
joblib.dump(vectorizer, os.path.join(BASE_DIR, "model", "email_vectorizer.pkl"))

print("Email Model Saved Successfully!")
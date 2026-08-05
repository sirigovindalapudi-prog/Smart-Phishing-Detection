<<<<<<< HEAD
import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Create model folder
os.makedirs("model", exist_ok=True)

# Load SMS Dataset
sms = pd.read_csv("dataset/sms_spam_dataset/spam.csv", encoding="latin-1")

# Keep only required columns
sms = sms.iloc[:, :2]
sms.columns = ["label", "message"]

# Convert labels
sms["label"] = sms["label"].map({
    "ham": 0,
    "spam": 1
})

# Features and Labels
X = sms["message"]
y = sms["label"]

# Convert text into numbers
vectorizer = TfidfVectorizer(stop_words="english")

X = vectorizer.fit_transform(X)

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train Model
model = MultinomialNB()
model.fit(X_train, y_train)

# Test Accuracy
pred = model.predict(X_test)

print("SMS Accuracy:", accuracy_score(y_test, pred))

# Save Model
joblib.dump(model, "model/sms_model.pkl")
joblib.dump(vectorizer, "model/sms_vectorizer.pkl")

=======
import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Create model folder
os.makedirs("model", exist_ok=True)

# Load SMS Dataset
sms = pd.read_csv("dataset/sms_spam_dataset/spam.csv", encoding="latin-1")

# Keep only required columns
sms = sms.iloc[:, :2]
sms.columns = ["label", "message"]

# Convert labels
sms["label"] = sms["label"].map({
    "ham": 0,
    "spam": 1
})

# Features and Labels
X = sms["message"]
y = sms["label"]

# Convert text into numbers
vectorizer = TfidfVectorizer(stop_words="english")

X = vectorizer.fit_transform(X)

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train Model
model = MultinomialNB()
model.fit(X_train, y_train)

# Test Accuracy
pred = model.predict(X_test)

print("SMS Accuracy:", accuracy_score(y_test, pred))

# Save Model
joblib.dump(model, "model/sms_model.pkl")
joblib.dump(vectorizer, "model/sms_vectorizer.pkl")

>>>>>>> 361e9d05fd57d5695edfe315ed97572f2ad94176
print("SMS Model Saved Successfully!")
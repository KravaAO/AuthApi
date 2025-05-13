import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# 1. Завантаження великого датасету
with open("column_dataset_labeled.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. Підготовка X та y
X = [" ".join(col["values"]) for col in data]
y = [col["column_name"] for col in data]

# 3. Поділ на train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

# 4. Побудова pipeline з TF-IDF + RandomForest
pipeline = make_pipeline(
    TfidfVectorizer(max_features=1000),
    RandomForestClassifier(n_estimators=150, random_state=42, n_jobs=-1)
)

# 5. Навчання моделі
pipeline.fit(X_train, y_train)

# 6. Оцінка на тесті
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))

# 7. Збереження моделі
joblib.dump(pipeline, "../app/utils/column_type_model_large.pkl")
print("✅ Model saved to column_type_model_large.pkl")

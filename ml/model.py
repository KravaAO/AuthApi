import joblib

model = joblib.load("../app/utils/column_type_model_large.pkl")
values = ["20-05-2024", "23-03-2033", "04-04-2004"]  # приклад колонки
text = " ".join(values)
predicted_type = model.predict([text])[0]
print(predicted_type)

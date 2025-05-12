import joblib
import os

this_dir = os.path.dirname(__file__)
model_path = os.path.join(this_dir, "column_type_model_large.pkl")
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Модель не знайдено за шляхом: {model_path}")
model = joblib.load(model_path)


def classify_columns_with_model(df):
    result = []
    for col in df.columns:
        values = df[col].dropna().astype(str).tolist()
        if not values:
            result.append("unknown")
            continue
        text = " ".join(values[:10])
        predicted = model.predict([text])[0]
        result.append(predicted)
    return result

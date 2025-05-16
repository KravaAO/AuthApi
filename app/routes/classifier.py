from flask import Blueprint, request, jsonify
import pandas as pd
from collections import Counter
from app.utils.classifier import classify_columns_with_model
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('classifier', __name__)

# 🔧 Функція для унікалізації назв
def make_column_names_unique(names):
    counter = Counter()
    unique_names = []
    for name in names:
        counter[name] += 1
        if counter[name] > 1:
            unique_names.append(f"{name}_{counter[name]}")
        else:
            unique_names.append(name)
    return unique_names

@bp.route('/classify-columns', methods=['POST'])
@jwt_required()
def classify_columns():
    try:
        data = request.get_json()
        print("📥 RAW incoming data:", data)

        raw_columns = data['data']
        print("📦 Parsed 'data' field:", raw_columns)

        merged = {}
        for column_dict in raw_columns:
            for key, value in column_dict.items():
                merged[key] = value
        print("📌 Merged keys:", list(merged.keys()))
        print("📌 Sample values:", {k: v[:2] for k, v in merged.items()})

        max_len = max(len(v) for v in merged.values())
        for key in merged:
            while len(merged[key]) < max_len:
                merged[key].append("")

        df = pd.DataFrame(merged)
        print("🟢 DEBUG: df created with shape", df.shape)
        print("🟢 DEBUG: df type:", type(df))
        print("🟢 DEBUG: df columns:", df.columns.tolist())
        print("🟢 DEBUG: df sample:\n", df.head(2))

        predicted_names = [str(name) for name in classify_columns_with_model(df)]
        print("🧠 Predicted column types:", predicted_names)

        # 🛡 Робимо назви колонок унікальними
        unique_names = make_column_names_unique(predicted_names)
        df.columns = unique_names
        print("✅ Renamed df.columns:", df.columns.tolist())

        result = {col: df[col].tolist() for col in df.columns}
        print("✅ Final result keys:", list(result.keys()))

        return jsonify({
            'columns': unique_names,
            'data': [result]
        })

    except Exception as e:
        print("❌ ERROR CAUGHT:", repr(e))
        return jsonify({'error': str(e)}), 500

from flask import Blueprint, request, jsonify
import pandas as pd
from app.utils.classifier import mock_classify_columns

bp = Blueprint('classifier', __name__)

@bp.route('/classify-columns', methods=['POST'])
def classify_columns():
    try:
        data = request.get_json()
        raw_columns = data['data']
        merged = {}
        for column_dict in raw_columns:
            for key, value in column_dict.items():
                merged[key] = value
        df = pd.DataFrame(zip(*merged.values()), columns=merged.keys())
        predicted_names = mock_classify_columns(df)
        df.columns = predicted_names
        result = {col: df[col].tolist() for col in df.columns}
        return jsonify({
            'columns': predicted_names,
            'data': [result]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
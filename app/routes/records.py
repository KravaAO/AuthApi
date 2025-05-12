from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Record, User
from app import db
import json

bp = Blueprint('records', __name__)

@bp.route('/api/upload', methods=['POST'])
@jwt_required()
def upload_data():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    for entry in data:
        existing_record = Record.query.filter_by(user_id=user.id, key=entry['key']).first()
        if existing_record:
            existing_record.value = json.dumps(entry['value'])
        else:
            new_record = Record(user_id=user.id, key=entry['key'], value=json.dumps(entry['value']))
            db.session.add(new_record)
    db.session.commit()
    return jsonify({'message': 'Data synchronized successfully'}), 200

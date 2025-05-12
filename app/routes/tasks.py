from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Task, User
from app import db
import json

bp = Blueprint('tasks', __name__)

@bp.route('/save', methods=['POST'])
@jwt_required()
def save():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({'message': 'Invalid data format: expected a list'}), 400
    task_data_json = json.dumps(data)
    new_task = Task(data=task_data_json, user_id=user.id)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': f'Data saved successfully for user {current_user}!'}), 201

@bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    tasks = Task.query.filter_by(user_id=user.id).all()
    tasks_list = [{'id': task.id, 'data': json.loads(task.data)} for task in tasks]
    return jsonify({'tasks': tasks_list}), 200
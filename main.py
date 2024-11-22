from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    config = db.Column(db.Text, nullable=True)
    selectors = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except:
        return jsonify({'message': 'Username already exists'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/save', methods=['POST'])
@jwt_required()
def save():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    task_name = data.get('task_name')
    status = data.get('status')
    config = data.get('config')
    selectors = data.get('selectors')

    if not task_name or not status:
        return jsonify({'message': 'Task name and status are required'}), 400

    try:
        # Конвертація у JSON
        config_json = json.dumps(config) if config else None
        selectors_json = json.dumps(selectors) if selectors else None

        new_task = Task(
            task_name=task_name,
            status=status,
            config=config_json,
            selectors=selectors_json,
            user_id=user.id
        )

        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': f'Task "{task_name}" saved successfully for user {current_user}!'}), 201
    except Exception as e:
        return jsonify({'message': 'Error saving task', 'error': str(e)}), 500
    #print(current_user, task_name, status, config, selectors)
    #return jsonify({'message': f'User {current_user} saved the task successfully!'}), 200

@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    tasks = Task.query.filter_by(user_id=user.id).all()

    tasks_list = [
        {
            'task_name': task.task_name,
            'status': task.status,
            'config': json.loads(task.config) if task.config else None,
            'selectors': json.loads(task.selectors) if task.selectors else None
        }
        for task in tasks
    ]

    return jsonify({'tasks': tasks_list}), 200


if __name__ == '__main__':
    if not os.path.exists('users.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)

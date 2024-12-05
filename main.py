from flask import send_file
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
import json

app = Flask(__name__)

# Налаштування Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'

# Додати підтримку CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:5123"}})

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Модель користувача
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

# Модель завдання
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Реєстрація користувача
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

# Авторизація користувача
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

# Збереження завдання
# Збереження завдання
@app.route('/save', methods=['POST'])
@jwt_required()
def save():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()

    # Перевірка типу даних на список
    if not isinstance(data, list):
        return jsonify({'message': 'Invalid data format: expected a list'}), 400

    try:
        # Збереження списку як JSON-рядок
        task_data_json = json.dumps(data)
        new_task = Task(
            data=task_data_json,
            user_id=user.id
        )

        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': f'Data saved successfully for user {current_user}!'}), 201
    except Exception as e:
        return jsonify({'message': 'Error saving task', 'error': str(e)}), 500



# Отримання завдань
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
            'id': task.id,
            'data': json.loads(task.data),
        }
        for task in tasks
    ]

    # Повернення результату як JSON
    return jsonify({'tasks': tasks_list}), 200

@app.route('/export_json/<int:task_id>', methods=['GET'])
@jwt_required()
def export_json(task_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    # Перевірка, чи існує користувач
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Логування користувача та запитуваного task_id
    print(f"Current user: {user.username}, user_id: {user.id}, requested task_id: {task_id}")

    # Знайти завдання за task_id та user_id поточного користувача
    task = Task.query.filter_by(id=task_id, user_id=user.id).first()

    if not task:
        return jsonify({'message': f'Task with id {task_id} not found for user {user.username}'}), 404

    # Формування JSON-даних для конкретного завдання
    task_data = {
        'id': task.id,
        'user_id': task.user_id,
        'data': json.loads(task.data)
    }

    # Назва файлу для експорту
    filename = f'user_{user.id}_task_{task_id}.json'

    # Запис у файл
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(task_data, json_file, ensure_ascii=False, indent=4)

    # Відправка файлу як відповідь
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    if os.path.exists('users.db'):
        os.remove('users.db')  # Видалити стару базу даних
    with app.app_context():
        db.create_all()  # Створити нову базу даних зі зміненою схемою
    app.run(debug=True, host='0.0.0.0', port=5001)


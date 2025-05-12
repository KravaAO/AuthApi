from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'
    CORS(app, resources={r"/*": {"origins": "http://localhost:5123"}})

    db.init_app(app)
    jwt.init_app(app)

    from app.routes import auth, tasks, records, classifier
    app.register_blueprint(auth.bp)
    app.register_blueprint(tasks.bp)
    app.register_blueprint(records.bp)
    app.register_blueprint(classifier.bp)

    with app.app_context():
        db.create_all()

    return app

from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os

from app.config import config

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app(config_name="default"):
    """Flask application factory."""
    app = Flask(__name__)

    # Load config
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.quiz import quiz_bp
    from app.routes.attempt import attempt_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(quiz_bp, url_prefix="/api/quiz")
    app.register_blueprint(attempt_bp, url_prefix="/api/attempt")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    # Serve frontend
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")

    @app.route("/")
    def serve_index():
        return send_from_directory(os.path.abspath(frontend_path), "index.html")

    @app.route("/<path:path>")
    def serve_static(path):
        if path.startswith("api/"):
            return {"error": "Not found"}, 404
        return send_from_directory(os.path.abspath(frontend_path), path)

    # Create tables
    with app.app_context():
        db.create_all()

    return app
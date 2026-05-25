from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db, bcrypt
from app.models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user account."""
    data = request.get_json()

    # Check if email already exists
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 409

    # Create new user
    user = User(
        full_name=data["full_name"],
        email=data["email"],
        role=data.get("role", "student")
    )
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Account created successfully",
        "user": user.to_dict()
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate user and return JWT token."""
    data = request.get_json()

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({
        "token": token,
        "user": user.to_dict()
    }), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """Logout current user."""
    return jsonify({"message": "Logged out successfully"}), 200
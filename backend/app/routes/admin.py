from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.quiz import Quiz
from app.models.attempt import Attempt

admin_bp = Blueprint("admin", __name__)

def is_admin():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return user and user.role == "admin"

@admin_bp.route("/stats", methods=["GET"])
@jwt_required()
def get_stats():
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403
    
    total_users = User.query.count()
    total_quizzes = Quiz.query.count()
    total_attempts = Attempt.query.count()
    
    return jsonify({
        "total_users": total_users,
        "total_quizzes": total_quizzes,
        "total_attempts": total_attempts
    }), 200

@admin_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403
    
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify({
        "users": [
            {
                "id": u.id,
                "full_name": u.full_name,
                "email": u.email,
                "role": u.role,
                "created_at": u.created_at.isoformat(),
                "quiz_count": Quiz.query.filter_by(user_id=u.id).count()
            }
            for u in users
        ]
    }), 200

@admin_bp.route("/quizzes", methods=["GET"])
@jwt_required()
def get_all_quizzes():
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403
    
    quizzes = Quiz.query.order_by(Quiz.created_at.desc()).all()
    return jsonify({
        "quizzes": [
            {
                "id": q.id,
                "title": q.title,
                "question_count": q.question_count,
                "created_at": q.created_at.isoformat(),
                "creator": User.query.get(q.user_id).full_name
            }
            for q in quizzes
        ]
    }), 200

@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

@admin_bp.route("/users/<int:user_id>/role", methods=["PATCH"])
@jwt_required()
def update_role(user_id):
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403
    
    from flask import request
    data = request.get_json()
    new_role = data.get("role")
    
    if new_role not in ["student", "lecturer", "admin"]:
        return jsonify({"error": "Invalid role"}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    user.role = new_role
    db.session.commit()
    return jsonify({"message": f"Role updated to {new_role}"}), 200
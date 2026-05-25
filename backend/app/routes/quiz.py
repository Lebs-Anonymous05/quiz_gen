from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.quiz import Quiz, Question
from app.models.user import User
from app.services.ai_service import generate_quiz
from app.services.pdf_service import extract_text_from_pdf
import secrets

quiz_bp = Blueprint("quiz", __name__)


@quiz_bp.route("/generate", methods=["POST"])
@jwt_required()
def generate():
    """Generate a quiz from lecture notes."""
    # Coming in Step 6 — AI integration
    return jsonify({"message": "Quiz generation coming soon"}), 200


@quiz_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_pdf():
    """Upload a PDF and extract text."""
    # Coming in Step 6 — PDF service
    return jsonify({"message": "PDF upload coming soon"}), 200


@quiz_bp.route("/", methods=["GET"])
@jwt_required()
def get_quizzes():
    """Get all quizzes for the current user."""
    user_id = get_jwt_identity()
    quizzes = Quiz.query.filter_by(user_id=user_id).all()
    return jsonify({"quizzes": [q.to_dict() for q in quizzes]}), 200


@quiz_bp.route("/<int:quiz_id>", methods=["GET"])
@jwt_required()
def get_quiz(quiz_id):
    """Get a specific quiz with its questions."""
    user_id = get_jwt_identity()
    quiz = Quiz.query.filter_by(id=quiz_id, user_id=user_id).first()

    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    return jsonify({
        "id": quiz.id,
        "title": quiz.title,
        "questions": [q.to_dict() for q in quiz.questions]
    }), 200


@quiz_bp.route("/<int:quiz_id>", methods=["DELETE"])
@jwt_required()
def delete_quiz(quiz_id):
    """Delete a quiz."""
    user_id = get_jwt_identity()
    quiz = Quiz.query.filter_by(id=quiz_id, user_id=user_id).first()

    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    db.session.delete(quiz)
    db.session.commit()

    return jsonify({"message": "Quiz deleted successfully"}), 200


@quiz_bp.route("/<int:quiz_id>/share", methods=["POST"])
@jwt_required()
def share_quiz(quiz_id):
    """Generate a shareable link for a quiz."""
    user_id = get_jwt_identity()
    quiz = Quiz.query.filter_by(id=quiz_id, user_id=user_id).first()

    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    if not quiz.share_token:
        quiz.share_token = secrets.token_urlsafe(32)
        db.session.commit()

    return jsonify({
        "share_url": f"/shared/{quiz.share_token}"
    }), 200


@quiz_bp.route("/shared/<token>", methods=["GET"])
def get_shared_quiz(token):
    """Access a shared quiz without authentication."""
    quiz = Quiz.query.filter_by(share_token=token).first()

    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    return jsonify({
        "id": quiz.id,
        "title": quiz.title,
        "questions": [q.to_dict() for q in quiz.questions]
    }), 200
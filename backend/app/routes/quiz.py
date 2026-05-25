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
    """Generate a quiz from lecture notes using Claude API."""
    user_id = get_jwt_identity()
    data = request.get_json()

    # Validate input
    title = data.get("title", "").strip()
    source_text = data.get("source_text", "").strip()
    question_count = data.get("question_count", 10)
    question_types = data.get("question_types", ["mcq"])

    if not title:
        return jsonify({"error": "Quiz title is required"}), 400
    if not source_text:
        return jsonify({"error": "Lecture notes are required"}), 400
    if not question_types:
        return jsonify({"error": "At least one question type is required"}), 400

    try:
        # Call Claude API
        raw_questions = generate_quiz(source_text, question_count, question_types)

        # Save quiz to database
        quiz = Quiz(
            user_id=user_id,
            title=title,
            source_text=source_text,
            question_count=len(raw_questions)
        )
        db.session.add(quiz)
        db.session.flush()  # Get quiz.id before committing

        # Save questions
        for index, q in enumerate(raw_questions):
            question = Question(
                quiz_id=quiz.id,
                question_type=q.get("type", "mcq"),
                question_text=q.get("question", ""),
                options=q.get("options"),
                correct_answer=q.get("correct_answer", ""),
                explanation=q.get("explanation", ""),
                order_index=index
            )
            db.session.add(question)

        db.session.commit()

        return jsonify({
            "quiz_id": quiz.id,
            "title": quiz.title,
            "questions": [q.to_dict() for q in quiz.questions]
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Quiz generation failed: {str(e)}"}), 500


@quiz_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_pdf():
    """Upload a PDF and extract text."""
    if "lecture_note" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["lecture_note"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported"}), 400

    # Save file temporarily
    import tempfile, os
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        from app.services.pdf_service import extract_text_from_pdf
        result = extract_text_from_pdf(tmp_path)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"PDF extraction failed: {str(e)}"}), 500
    finally:
        os.unlink(tmp_path)


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
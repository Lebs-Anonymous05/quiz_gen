from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.attempt import Attempt
from app.models.quiz import Quiz, Question

attempt_bp = Blueprint("attempt", __name__)


@attempt_bp.route("/<int:quiz_id>", methods=["POST"])
@jwt_required()
def submit_attempt(quiz_id):
    """Submit a completed quiz attempt and return score."""
    user_id = get_jwt_identity()
    data = request.get_json()

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    user_answers = data.get("answers", {})
    time_taken = data.get("time_taken", None)

    # Calculate score
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    correct = 0
    results = []

    for question in questions:
        user_answer = user_answers.get(str(question.id), "")
        is_correct = user_answer.strip().lower() == question.correct_answer.strip().lower()
        if is_correct:
            correct += 1
        results.append({
            "question_id": question.id,
            "your_answer": user_answer,
            "correct_answer": question.correct_answer,
            "is_correct": is_correct,
            "explanation": question.explanation
        })

    score = (correct / len(questions)) * 100 if questions else 0

    # Save attempt
    attempt = Attempt(
        user_id=user_id,
        quiz_id=quiz_id,
        score=round(score, 2),
        answers=user_answers,
        time_taken=time_taken
    )
    db.session.add(attempt)
    db.session.commit()

    return jsonify({
        "score": round(score, 2),
        "correct": correct,
        "total": len(questions),
        "results": results
    }), 201


@attempt_bp.route("/history", methods=["GET"])
@jwt_required()
def get_history():
    """Get all quiz attempts for the current user."""
    user_id = get_jwt_identity()
    attempts = Attempt.query.filter_by(user_id=user_id).all()

    return jsonify({
        "attempts": [
            {
                "attempt_id": a.id,
                "quiz_title": a.quiz.title,
                "score": a.score,
                "completed_at": a.completed_at.isoformat()
            }
            for a in attempts
        ]
    }), 200
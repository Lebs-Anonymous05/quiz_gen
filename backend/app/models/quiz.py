from datetime import datetime
from app import db


class Quiz(db.Model):
    """Quiz model — stores generated quizzes."""
    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    source_text = db.Column(db.Text, nullable=False)
    question_count = db.Column(db.Integer, nullable=False)
    share_token = db.Column(db.String(64), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    questions = db.relationship("Question", backref="quiz", lazy=True, cascade="all, delete-orphan")
    attempts = db.relationship("Attempt", backref="quiz", lazy=True)

    def to_dict(self):
        """Serialize quiz to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "question_count": self.question_count,
            "created_at": self.created_at.isoformat(),
            "share_token": self.share_token
        }


class Question(db.Model):
    """Question model — stores individual quiz questions."""
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    question_type = db.Column(db.String(20), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON, nullable=True)
    correct_answer = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    order_index = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        """Serialize question to dictionary."""
        return {
            "id": self.id,
            "type": self.question_type,
            "question": self.question_text,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "explanation": self.explanation,
            "order_index": self.order_index
        }
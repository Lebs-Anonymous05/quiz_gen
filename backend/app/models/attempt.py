from datetime import datetime
from app import db


class Attempt(db.Model):
    """Attempt model — records each quiz attempt by a user."""
    __tablename__ = "attempts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    score = db.Column(db.Float, nullable=False)
    answers = db.Column(db.JSON, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    time_taken = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        """Serialize attempt to dictionary."""
        return {
            "id": self.id,
            "quiz_id": self.quiz_id,
            "score": self.score,
            "completed_at": self.completed_at.isoformat(),
            "time_taken": self.time_taken
        }
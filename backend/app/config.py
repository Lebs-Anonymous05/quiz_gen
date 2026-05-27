import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max upload
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)


class DevelopmentConfig(Config):
    """Development configuration — uses SQLite locally."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///quizgen_dev.db"
    )


class ProductionConfig(Config):
    """Production configuration — uses PostgreSQL."""
    DEBUG = False
    db_url = os.getenv("DATABASE_URL", "")
    SQLALCHEMY_DATABASE_URI = db_url.replace("postgres://", "postgresql://", 1) if db_url else None


class TestingConfig(Config):
    """Testing configuration — uses in-memory SQLite."""
    TESTING = True
    FLASK_ENV = "testing"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "test-jwt-secret-key-that-is-long-enough-32chars"
    SECRET_KEY = "test-secret-key-that-is-long-enough-32chars"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}
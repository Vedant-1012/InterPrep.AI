"""
Configuration settings for InterPrep-AI Next Generation.
"""
import os
from datetime import timedelta
from pathlib import Path

# Absolute path to project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "interprep.db"

class Config:
    """Base configuration."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-please-change-in-production')
    
    # Database settings - Use absolute path to SQLite DB
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{DB_PATH}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-dev-key-please-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # AI settings
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', 'AIzaSyBRSItdXPL8ATgKNngUXxSPU3NjbHnaFJU')
    GENERATIVE_MODEL_NAME = 'gemini-1.5-flash'
    EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'
    
    # CORS settings
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5001']


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=10)


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    
    # In production, ensure these are set in environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{DB_PATH}")
    
    # Production CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
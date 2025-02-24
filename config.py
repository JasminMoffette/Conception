import os

class Config:
    """Configuration générale de l'application Flask"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super_secret_key')

    # Configuration de la base de données (SQLite par défaut)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

class Config:
    """Configuration générale de l'application Flask"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super_secret_key')

    # Définir le dossier de base et le dossier instance
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    INSTANCE_FOLDER = os.path.join(BASE_DIR, 'instance')

    # Configurer l'URI de la base de données pour utiliser le fichier inventaire.db dans le dossier instance
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{os.path.join(INSTANCE_FOLDER, "inventaire.db")}')

    # Chemin de base du projet
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Dossier contenant les fichiers de données
    DATA_FOLDER = os.path.join(BASE_DIR, 'data')

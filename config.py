import os

class Config:
    # Récupération des variables d'environnement
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_NAME = os.environ.get('DB_NAME', 'test_db')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
    
    # Construction de l'URI de connexion SQLAlchemy
    # Format: mysql+pymysql://user:password@host/db_name
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    
    # Désactiver le tracking des modifications pour optimiser les performances
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Clé secrète pour les sessions (à sécuriser en prod)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')

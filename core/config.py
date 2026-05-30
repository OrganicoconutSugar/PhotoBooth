import os

class Config:
    SECRET_KEY = 'kunci_rahasia_photobooth_lucu_123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join('static', 'uploads')

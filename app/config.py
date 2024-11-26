import os

class Config:
    # Cấu hình SQLite cho Heroku
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///database.db')  # Lấy từ môi trường Heroku
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)

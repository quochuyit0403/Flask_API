import os

class Config:
    # Cấu hình SQLite cho Heroku
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///database.db')  # Lấy từ môi trường Heroku
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = os.urandom(24)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Đường dẫn tuyệt đối tới thư mục chứa config.py
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)

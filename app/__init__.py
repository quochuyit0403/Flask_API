# khởi tạo ứng dụng Flask và thiết lập các cấu hình cơ bản

from flask import Flask
from .extensions import db
from .routes import api
import os

def create_app():
    app = Flask(__name__)

    # Cấu hình cơ sở dữ liệu, sử dụng PostgreSQL nếu có, nếu không thì dùng SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Khoi tao SQLAlchemy
    db.init_app(app)

    # Đăng ký blueprint cho các route
    app.register_blueprint(api)

    with app.app_context():
        db.create_all()  # Tạo các bảng dựa trên model đã định nghĩa

    return app

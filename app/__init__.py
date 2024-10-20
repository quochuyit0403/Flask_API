# khởi tạo ứng dụng Flask và thiết lập các cấu hình cơ bản

from flask import Flask
from .extensions import db
from .routes import api

def create_app():
    app = Flask(__name__)

    # Doc cau hinh tu config.py, trong đó có cấu hình connect db
    app.config.from_object('app.config.Config')

    # Khoi tao SQLAlchemy
    db.init_app(app)

    # Dang ki blueprint cho cac route
    app.register_blueprint(api)

    with app.app_context():
        db.create_all()  # Tạo các bảng dựa trên model đã định nghĩa

    return app
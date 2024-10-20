# Cấu hình cho ứng dụng, bao gồm thông tin kết nối tới MySQL.

import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/flask_api'
    SQLALCHEMY_TRACK_MODIFICATIONS = False # tắt tính năng theo dõi
    SECRET_KEY = os.urandom(24)
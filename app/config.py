# Cấu hình cho ứng dụng, bao gồm thông tin kết nối tới MySQL.
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://root:@localhost/flask_api')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "levanquochuyphanbaokhangdeptraivaio"

# Định nghĩa các API endpoint (route) để trả về dữ liệu JSON.
from flask import Blueprint, jsonify
from .models import User, Task
from .extensions import db

# Khởi tạo blueprint để định nghĩa các route cho API 
api = Blueprint('api', __name__)

@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{
        'id': user.id, 'name': user.fullname, 'age': user.age,
        'gender': user.gender, 'phone': user.phone, 'address': user.address,
        'email': user.email, 'username': user.username, 'password': user.password,
        'avatar': user.avatar, 'create_at': user.create_at          
    } for user in users]

    return jsonify(user_list)

@api.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_list = [{
        'id': task.id, 'title': task.title, 'user_id': task.user_id,
        'description': task.description, 'priority': task.priority, 
        'status': task.status, 'begin_day': task.begin_day, 
        'due_day': task.due_day, 
    } for task in tasks]
    return jsonify(task_list)
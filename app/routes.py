# Định nghĩa các API endpoint (route) để trả về dữ liệu JSON.
from flask import Blueprint, jsonify, request
from .models import User, Task, Project, TaskPriority, TaskStatus
from .extensions import db
from datetime import datetime

# Khởi tạo blueprint để định nghĩa các route cho API 
api = Blueprint('api', __name__)


# Phần nhiệm vụ
@api.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_list = [{
        'id': task.id, 'title': task.title, 'user_id': task.user_id, 'project_id': task.project_id,
        'description': task.description, 
        'priority': task.priority.name if hasattr(task.priority, 'name') else task.priority, 
        'status': task.status.name if hasattr(task.status, 'name') else task.status,
        'begin_day': task.begin_day, 
        'due_day': task.due_day, 
    } for task in tasks]
    return jsonify(task_list)

# Thêm mới 1 task
@api.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()

    try:
        new_task = Task(
            user_id=data['user_id'],
            project_id=data['project_id'],
            title=data['title'],
            description=data['description'],
            status=TaskStatus[data['status']],  # Chuyển chuỗi sang enum TaskStatus
            begin_day=data['begin_day'],
            due_day=data['due_day'],
            priority=TaskPriority[data['priority']]  # Chuyển chuỗi sang enum TaskPriority
        )

        db.session.add(new_task)
        db.session.commit()

        return jsonify({"message": "Task added successfully"}), 201

    except KeyError as e:
        return jsonify({"error": f"Key error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Xóa task theo ID
@api.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    try:
        task = Task.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': "Task deleted successfully"})
    except KeyError as e:
        return jsonify({"error": f"Key error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Cập nhật task = id
@api.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    try:
        task = Task.query.get_or_404(id)
        data = request.get_json()
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.status = TaskStatus[data['status'].upper()] if 'status' in data else task.status
        task.priority = TaskPriority[data['priority'].upper()] if 'priority' in data else task.priority
        task.begin_day = datetime.strptime(data['begin_day'], '%Y-%m-%d') if 'begin_day' in data else task.begin_day
        task.due_day = datetime.strptime(data['due_day'], '%Y-%m-%d') if 'due_day' in data else task.due_day
        db.session.commit()
        return jsonify({"message": "Task updated successfully"})
    except KeyError as e:
        return jsonify({"error": f"Key error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Tìm kiếm task = tiêu đề
@api.route('/tasks/search', methods=['GET'])
def search_tasks():
    title_query = request.args.get('title', '')
    tasks = Task.query.filter(Task.title.ilike(f'%{title_query}%')).all()
    task_list = [{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status.name,
        'priority': task.priority.name,
        'begin_day': task.begin_day,
        'due_day': task.due_day,
        'user_id': task.user_id,
        'project_id': task.project_id
    } for task in tasks]
    return jsonify(task_list)

    
# Phần users
@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{
        'id': user.id, 'fullname': user.fullname, 'age': user.age,
        'gender': user.gender, 'phone': user.phone, 'address': user.address,
        'email': user.email, 'username': user.username, 'password': user.password,
        'avatar': user.avatar, 'create_at': user.create_at          
    } for user in users]

    return jsonify(user_list)

@api.route('/users', methods=['POST'])
def addUsers():
    data = request.get_json()
    try:

        new_user = User(
            fullname = data['fullname'],
            age = data['age'],
            gender = data['gender'],
            phone = data['phone'],
            address = data['address'],
            email = data['email'],
            username = data['username'],
            password = data['password'],
            avatar = data['avatar'],
            create_at = data['create_at'],
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User added successfully"}), 201
    
    except KeyError as e:
        return jsonify({"error": f"Key error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Xóa users theo id   
@api.route('/users/<int:id>', methods=['DELETE'])
def deleteUser(id):
    try:
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})

    except KeyError as e:
        return jsonify({"error": f"Key error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Cap nhat user theo id
@api.route('/users/<int:id>', methods=['PUT'])
def updateUser(id):
    try:
        user = User.query.get_or_404(id)
        data = request.get_json()
        
        user.fullname = data.get('fullname', user.fullname)
        user.age = data.get('age', user.age)
        user.address = data.get('address', user.address)
        user.email = data.get('email', user.email)
        user.gender = data.get('gender', user.gender)
        user.avatar = data.get('avatar', user.avatar)
        user.password = data.get('password', user.password)
        user.phone = data.get('phone', user.phone)
        user.username = data.get('username', user.username)
        user.create_at = data.get('create_at', user.create_at)
        db.session.commit()
        return jsonify({"message": "User updated successfully"})

    except KeyError as e:
        return jsonify({"error": f"Key error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Tim kiem bang ten:
@api.route('/users/search', methods=['GET'])
def searchUser():
    name_query = request.args.get('fullname', '')
    users = User.query.filter(User.fullname.ilike(f'%{name_query}%')).all()
    user_list = [{
        "address": user.address,
        "age": user.age,
        "avatar": user.avatar,
        "create_at": user.create_at,
        "email": user.email,
        "fullname": user.fullname,
        "gender": user.gender,
        "id": user.id,
        "password": user.password,
        "phone": user.phone,
        "username": user.username
    } for user in users]
    return jsonify(user_list)

# Đó là kiểu viết code với list comprehension của vòng for:
# numbers = [1, 2, 3, 4, 5]
# squares = [x**2 for x in numbers]  # Tạo list các bình phương của từng số
# print(squares)  # Kết quả: [1, 4, 9, 16, 25]


# Phần projects
@api.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    project_list = [{
        'id': project.id,
        'user_id': project.user_id,
        'name': project.name,
        'description': project.description,
        'created_at': project.created_at,
        'updated_at': project.updated_at
    } for project in projects]
    return jsonify(project_list)

# Thêm mới 1 project
@api.route('/projects', methods=['POST'])
def add_project():
    data = request.get_json()

    try:
        new_project = Project(
            user_id=data['user_id'],
            name=data['name'],
            description=data['description'],
            created_at=data['created_at'],
            updated_at=data['updated_at'],
        )

        db.session.add(new_project)
        db.session.commit()

        return jsonify({"message": "Project added successfully"}), 201

    except KeyError as e:
        return jsonify({"error": f"Key error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Xóa project theo ID
@api.route('/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    try:
        project = Project.query.get_or_404(id)
        db.session.delete(project)
        db.session.commit()
        return jsonify({'message': "Project deleted successfully"})
    except KeyError as e:
        return jsonify({"error": f"Key error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Cập nhật project = id
@api.route('/projects/<int:id>', methods=['PUT'])
def update_project(id):
    try:
        project = Project.query.get_or_404(id)
        data = request.get_json()
        project.name = data.get('name', project.name)
        project.description = data.get('description', project.description)
        project.created_at = datetime.strptime(data['created_at'], '%Y-%m-%d') if 'created_at' in data else project.created_at
        project.updated_at = datetime.strptime(data['updated_at'], '%Y-%m-%d') if 'updated_at' in data else project.updated_at
        db.session.commit()
        return jsonify({"message": "Project updated successfully"})
    except KeyError as e:
        return jsonify({"error": f"Key error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Tìm kiếm project = tiêu đề
@api.route('/projects/search', methods=['GET'])
def search_projects():
    name_query = request.args.get('name', '')
    projects = Project.query.filter(Project.name.ilike(f'%{name_query}%')).all()
    project_list = [{
        'id': project.id,
        'user_id': project.user_id,
        'name': project.name,
        'description': project.description,
        'created_at': project.created_at,
        'updated_at': project.updated_at
    } for project in projects]
    return jsonify(project_list)

# Định nghĩa các API endpoint (route) để trả về dữ liệu JSON.
from flask import Blueprint, jsonify, request
from .models import User, Task, Project, TaskPriority, TaskStatus, UserHost
from .extensions import db
from datetime import datetime
from system_info import get_system_info
# Khởi tạo blueprint để định nghĩa các route cho API
api = Blueprint('api', __name__)



# Phần nhiệm vụ
@api.route('/', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_list = [{
        'id': task.id, 'title': task.title, 'user_id': task.user_id, 'project_id': task.project_id,
        'description': task.description,
        'priority': task.priority.name if hasattr(task.priority, 'name') else task.priority,
        'status': task.status.name if hasattr(task.status, 'name') else task.status,
        'begin_day': task.begin_day,
        'due_day': task.due_day
    } for task in tasks]
    return jsonify({
        'Tasks list': task_list
    })


@api.route('/tasks/<int:user_id>', methods=['GET'])
def get_tasks_by_user_id(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()
    task_list = [{
        'id': task.id,
        'title': task.title,
        'user_id': task.user_id,
        'project_id': task.project_id,
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
    data = request.form
    
    try:
        # Chuyển đổi chuỗi ngày tháng
        begin_day = datetime.strptime(data['begin_day'], '%a, %d %b %Y %H:%M:%S GMT').date()
        due_day = datetime.strptime(data['due_day'], '%a, %d %b %Y %H:%M:%S GMT').date()
        
        # Tạo task mới
        new_task = Task(
            user_id=data['user_id'],
            project_id=data['project_id'],
            title=data['title'],
            description=data['description'],
            status=TaskStatus[data['status']],
            begin_day=begin_day,
            due_day=due_day,
            priority=TaskPriority[data['priority']]
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
        task.status = TaskStatus[data['status'].upper(
        )] if 'status' in data else task.status
        task.priority = TaskPriority[data['priority'].upper(
        )] if 'priority' in data else task.priority
        task.begin_day = datetime.strptime(
            data['begin_day'], '%Y-%m-%d') if 'begin_day' in data else task.begin_day
        task.due_day = datetime.strptime(
            data['due_day'], '%Y-%m-%d') if 'due_day' in data else task.due_day
        db.session.commit()
        return jsonify({"message": "Task updated successfully"})
    except KeyError as e:
        return jsonify({"error": f"Key error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Tìm kiếm task = tiêu đề


@api.route('/tasks/search/<int:user_id>', methods=['GET'])
def search_tasks(user_id):
    # Lấy giá trị tìm kiếm từ query string
    title_query = request.args.get('title', '')

    # Lọc các task theo user_id và title_query
    tasks = Task.query.filter(
        Task.user_id == user_id,
        Task.title.ilike(f'%{title_query}%')
    ).all()

    # Chuyển đổi kết quả truy vấn thành danh sách các dictionary
    task_list = [{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status.name if hasattr(task.status, 'name') else task.status,
        'priority': task.priority.name if hasattr(task.priority, 'name') else task.priority,
        'begin_day': task.begin_day,
        'due_day': task.due_day,
        'user_id': task.user_id,
        'project_id': task.project_id
    } for task in tasks]

    # Trả về kết quả dưới dạng JSON
    return jsonify(task_list)


# Phần users
@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{
        'id': user.id, 'fullname': user.fullname, 'age': user.age,
        'gender': user.gender, 'phone': user.phone, 'address': user.address,
        'email': user.email, 'username': user.username, 'password': user.password,
        'avatar': user.avatar, 'create_at': user.create_at, 'isOnline': user.isOnline, 
        'isActive': user.isActive
    } for user in users]

    # Đếm số lượng on, off
    online_count = sum(1 for user in users if user.isOnline)
    offline_count = len(users) - online_count

    return jsonify({
        'users': user_list,
        'online_count': online_count,
        'offline_count': offline_count
    })


@api.route('/users', methods=['POST'])
def addUsers():
    data = request.get_json()
    try:
        create_at = datetime.strptime(data['create_at'], '%a, %d %b %Y %H:%M:%S GMT').date()
        new_user = User(
            fullname=data['fullname'],
            age=data['age'],
            gender=data['gender'],
            phone=data['phone'],
            address=data['address'],
            email=data['email'],
            username=data['username'],
            password=data['password'],
            avatar=data['avatar'],
            create_at=create_at,
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

# isOnline


@api.route('/users/<int:user_id>/status', methods=['PUT'])
def update_user_status(user_id):
    data = request.json
    user = User.query.get(user_id)

    if user:
        user.isOnline = data.get('isOnline', False)
        db.session.commit()
        return jsonify({'message': 'Trạng thái người dùng đã được cập nhật!'}), 200

    return jsonify({'message': 'Không tìm thấy người dùng!'}), 404

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
    return jsonify(
        {'Project List': project_list}
    )


@api.route('/projects/<int:user_id>', methods=['GET'])
def get_projects_by_user_id(user_id):
    projects = Project.query.filter_by(user_id=user_id).all()
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
    print(f"Received data: {data}")

    try:
        created_at = datetime.strptime(data['created_at'], '%a, %d %b %Y %H:%M:%S GMT').date()
        updated_at = datetime.strptime(data['updated_at'], '%a, %d %b %Y %H:%M:%S GMT').date()

        new_project = Project(
            user_id=data['user_id'],
            name=data['name'],
            description=data['description'],
            created_at=created_at,
            updated_at=updated_at,
        )

        db.session.add(new_project)
        print("Added project to session")
        db.session.commit()
        print("Committed to database")

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
        project.created_at = datetime.strptime(
            data['created_at'], '%Y-%m-%d') if 'created_at' in data else project.created_at
        project.updated_at = datetime.strptime(
            data['updated_at'], '%Y-%m-%d') if 'updated_at' in data else project.updated_at
        db.session.commit()
        return jsonify({"message": "Project updated successfully"})
    except KeyError as e:
        return jsonify({"error": f"Key error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Tìm kiếm project = tiêu đề


@api.route('/projects/search/<int:user_id>', methods=['GET'])
def search_projects(user_id):
    name_query = request.args.get('name', '')

    projects = Project.query.filter(
        Project.user_id == user_id,
        Project.name.ilike(f'%{name_query}%')
    ).all()

    project_list = [{
        'id': project.id,
        'user_id': project.user_id,
        'name': project.name,
        'description': project.description,
        'created_at': project.created_at,
        'updated_at': project.updated_at
    } for project in projects]
    return jsonify(project_list)


# ==========SYSTEM INFO================
@api.route('/system_info', methods=['GET'])
def system_info():
    info = get_system_info()
    return jsonify(info)

# ==========USER HOST================
@api.route('/user_host', methods=['GET'])
def get_all_host():
    hosts = UserHost.query.all()
    host_list = [{
        'id': h.id,
        'client_ip': h.client_ip,
        'success': h.success,
        'fail': h.fail,
        'created_at': h.created_at,
        'updated_at': h.updated_at
    } for h in hosts]
    return jsonify(host_list)

@api.route('/user_host/<string:client_ip>', methods=['GET'])
def get_host_by_ip(client_ip):
    host = UserHost.query.filter_by(client_ip=client_ip).first()
    user_host_data = {
        'id': host.id,
        'client_ip': host.client_ip,
        'success': host.success,
        'fail': host.fail,
        'created_at': host.created_at,
        'updated_at': host.updated_at
    }
    print(type(user_host_data['created_at']))
    return jsonify(user_host_data)


@api.route('/user_host', methods=['POST'])
def add_host():
    data = request.get_json()
    
    try:
        # Chuyển đổi chuỗi ngày/giờ sang kiểu date
        created_at_date = datetime.strptime(data['created_at'], "%a, %d %b %Y %H:%M:%S %Z").date()
        updated_at_date = datetime.strptime(data['updated_at'], "%a, %d %b %Y %H:%M:%S %Z").date()
        # Kiểm tra xem host đã tồn tại chưa
        existing_host = UserHost.query.filter_by(
            client_ip=data['client_ip']).first()
        if existing_host:
            # Nếu đã tồn tại, chỉ cần cập nhật
            existing_host.success = data.get('success', 0)
            existing_host.fail = data.get('fail', 0)
            existing_host.created_at = created_at_date
            existing_host.updated_at = updated_at_date
            db.session.commit()
            return jsonify({"message": "Host updated successfully"}), 200

        # Nếu chưa tồn tại, thêm mới
        new_host = UserHost(
            client_ip=data['client_ip'],
            success=data.get('success', 0),  # Mặc định là 0 nếu không có
            fail=data.get('fail', 0),
            created_at=created_at_date,
            updated_at=updated_at_date
        )

        db.session.add(new_host)
        db.session.commit()

        return jsonify({"message": "host added successfully"}), 201

    except KeyError as e:
        return jsonify({"error": f"Key error: {str(e)}"}), 400
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        print(type(created_at_date))
        print(type(updated_at_date))
        


@api.route('/user_host/<string:client_ip>/status', methods=['PUT'])
def update_request(client_ip):
    data = request.json
    host = UserHost.query.filter_by(client_ip=client_ip).first()
    print(host)
    if host:
        if data.get('isSuccess'):
            host.success += 1
            db.session.commit()
        else:
            host.fail += 1
            db.session.commit()
        return jsonify({'message': 'User Host updated!'}), 200

    return jsonify({'message': 'Không tìm thấy người dùng!'}), 404

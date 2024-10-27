# Khai báo các bảng và mối quan hệ trong cơ sở dữ liệu.

from .extensions import db
import enum

# Định nghĩa enum cho 1 trạng thái task
class TaskStatus(enum.Enum):
    TOTO = 'todo',
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

# Định nghĩa enum cho muc do uu tien của task
class TaskPriority(enum.Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    avatar = db.Column(db.String(1000), nullable=False)
    create_at = db.Column(db.Date, nullable=False)

    # Thiet lap moi quan he 1-n
    tasks = db.relationship('Task', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    projects = db.relationship('Project', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    
class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(100), nullable=False)
    is_read = db.Column(db.Boolean, nullable=False)
    create_at = db.Column(db.Date, nullable=False)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Enum(TaskStatus), nullable=False, default=TaskStatus.TOTO)
    begin_day = db.Column(db.Date, nullable=False)
    due_day = db.Column(db.Date, nullable=False)
    priority = db.Column(db.Enum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM)

    # Thiet lap moi quan he 1-n
    attachments = db.relationship('Attachment', backref='task', lazy=True)
    comments = db.relationship('Comment', backref='task', lazy=True)

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.Date, nullable=False)
    updated_at = db.Column(db.Date, nullable=False)

    # Thiet lap moi quan he 1-n
    tasks = db.relationship('Task', backref='project', lazy=True)
    

class Attachment(db.Model):
    __tablename__ = 'attachments'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    file_path = db.Column(db.String(1000), nullable=False)
    create_at = db.Column(db.Date, nullable=False)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    create_at = db.Column(db.Date, nullable=False)
    

import email
from main import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(db.Model,UserMixin):
    __tablename__="users"

    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.Text(),unique=True,nullable=False)
    email=db.Column(db.Text(),unique=True,nullable=False)
    password=db.Column(db.Text(),unique=True,nullable=False)
    blogs=db.relationship("Blog",backref="users",lazy=True)

    def __init__(self,name,email,password):
        self.name=name
        self.email=email
        self.password=generate_password_hash(password)

    def __repr__(self):
        return self.name

    def check_password(self,password):
        return check_password_hash(self.password,password)

class Blog(db.Model):
    __tablename__="blogs"

    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.Text(),nullable=False)
    content=db.Column(db.Text(),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    created_by=db.Column(db.Text(),nullable=False)
    time=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __init__(self,title,content,user_id,created_by,time):
        self.title=title
        self.content=content
        self.user_id=user_id
        self.created_by=created_by
        self.time=time

class Feedback(db.Model):
    __tablename__="feedback"
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.Text(),nullable=False)
    feedback=db.Column(db.Text(),nullable=False)

    def __init__(self,email,feedback):
        self.email=email
        self.feedback=feedback

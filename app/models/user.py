from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    pwd = Column(String(128), nullable=False)

    # Usado após cadastrado
    def __init__(self, email, pwd):
        self.email = email
        self.pwd = pwd
    

class UserProfile(db.Model):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(120), nullable=False)
    profile_img = Column(String(250), nullable=True)
    confirmed = Column(Boolean, default=False, nullable=False)
    unci_student = Column(Boolean, default=False, nullable=False)
    matricula = Column(String(100), nullable=True, default='')
    curso = Column(String(100), nullable=True, default='')
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(), default=datetime.datetime.now(datetime.UTC))

    def __init__(self, user_id, name, profile_img: str = "", confirmed=False, unci_student=False, matricula="", curso="", active=True, created_at=datetime.datetime.now(datetime.UTC)):
        self.user_id = user_id
        self.name = name
        self.profile_img = profile_img
        self.confirmed = confirmed
        self.unci_student = unci_student
        self.matricula = matricula
        self.curso = curso
        self.active = active
        self.created_at = created_at

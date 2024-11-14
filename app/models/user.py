from app import db, bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, event
from flask_login import UserMixin
import datetime
import os
import uuid


def current_time():
    return datetime.datetime.now(datetime.timezone.utc)


class User(db.Model, UserMixin):
    """Modelo para CRUD de usuários
        Variáveis existentes:
        - email
        - pwd
    """

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    pwd = Column(String(128), nullable=False)

    def verify_pwd(self, check_pwd):
        return bcrypt.check_password_hash(self.pwd, check_pwd)


class UserType(db.Model):
    __tablename__ = 'user_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)


def generate_img_name(file):
        if not file:
            return '0'
        
        ext = os.path.splitext(file)[-1]
        uuid_id = uuid.uuid4()
        return f"{uuid_id}{ext}"


class UserProfile(db.Model):
    """ Modelo para CRUD do perfil do usuário

    variáveis existentes:
    - user_id: integer
    - first_name
    - last_name
    - profile_img: receber string
    - confimed
    - unci_student
    - matricula
    - curso
    - active
    - created_at
    - updated_at
    """

    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"),
                     unique=True, nullable=False)
    first_name = Column(String(120), nullable=False, default="Primeiro nome")
    last_name = Column(String(120), nullable=False, default='Sobrenome')
    profile_img = Column(String(250), nullable=False, default='no image')
    confirmed = Column(Boolean, default=False, nullable=False)
    user_type = Column(Integer, ForeignKey("user_types.id"), nullable=True)
    curso = Column(String(100), nullable=True, default='não aluno')
    active = Column(Boolean, nullable=False, default=True)
    completed = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(), default=current_time, nullable=False)
    updated_at = Column(DateTime(), default=current_time, nullable=False)
    
    def __init__(self, user_id, first_name, last_name, user_type, profile_img='', curso=None,):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.profile_img = generate_img_name(profile_img)
        self.user_type = user_type
        self.curso = curso

    def get_fullname(self):
        return self.first_name + self.last_name
    
    def get_email(self):
        return User.query.filter_by(id=self.user_id).first().email
    
    def set_img(self, img):
        self.profile_img = generate_img_name(img)


@event.listens_for(UserProfile, 'before_update')
def update_time(mapper, connection, target):
    target.update_at = current_time()

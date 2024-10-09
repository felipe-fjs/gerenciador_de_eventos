from app import db, bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, event
import datetime

def current_time():
    return datetime.datetime.now(datetime.timezone.utc)

class User(db.Model):
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
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    name = Column(String(120), nullable=False)
    profile_img = Column(String(250), nullable=True)
    confirmed = Column(Boolean, default=False, nullable=False)
    unci_student = Column(Boolean, default=False, nullable=False)
    matricula = Column(String(100), nullable=True, default='')
    curso = Column(String(100), nullable=True, default='')
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(), default=current_time, nullable=False)
    updated_at = Column(DateTime(), default=current_time, nullable=False)


@event.listens_for(UserProfile, 'before_update')
def update_time(mapper, connection, target):
    target.update_at = current_time()

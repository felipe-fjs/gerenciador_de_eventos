from app import db, app
from flask_login import current_user
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, event, UniqueConstraint, func
import datetime


def current_time():
    return datetime.datetime.now(datetime.timezone.utc)

class ColabRole(db.Model):
    __tablename__ = 'colab_roles'

    id = Column(Integer, primary_key=True)
    role = Column(String(60), nullable=False)
    permission_level = Column(Integer, unique=True, nullable=False)
    created_at = Column(DateTime(), default=current_time, nullable=False)
    update_at = Column(DateTime(), default=current_time, nullable=False)

    @classmethod
    def next_permission_level(cls):
        "Retorna o próximo valor inteiro da tabela de permissões de acesso"
        quant_roles = db.session.query(func.count(cls.permission_level)).scalar()
        return quant_roles + 1

    def __init__(self, role):
        self.role = role
        self.permission_level = ColabRole.next_permission_level()

class Colab(db.Model):
    __tablename__ = 'colabs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    is_coor = Column(Boolean(), nullable=False, default=False)
    active = Column(Boolean(), nullable=False, default=True)


class ColabArea(db.Model):
    __tablename__ = 'colab_areas'

    id = Column(Integer, primary_key=True)
    name = Column(String(60), unique=True, nullable=False)


class EventColab(db.Model):
    __tablename__ = 'event_colabs'

    id = Column(Integer, primary_key=True)
    role = Column(Integer, ForeignKey('colab_roles.id'), nullable=False)
    area = Column(Integer, ForeignKey('colab_areas.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)

    __table_args__ = (UniqueConstraint('user_id', 'event_id', name="colab_already_in_this_event"),)

    def take_role(self):
        return ColabRole.query.filter_by(id=self.role).first().role
    
    def take_area(self):
        return ColabArea.query.filter_by(id=self.area).first().name

class SubEventColab(db.Model):
    __tablename__ = 'sub_event_colabs'

    id = Column(Integer, primary_key=True)
    event_colab_id = Column(Integer, ForeignKey('event_colabs.id'), nullable=False)
    sub_event_id = Column(Integer, ForeignKey('sub_events.id'), nullable=False)

    __table_args__ = (UniqueConstraint('event_colab_id', 'sub_event_id', name="colab_already_in_this_sub_event"),)


@event.listens_for(ColabRole, 'before_update')
def update_time(mapper, connection, target):
    target.update_at = current_time()


@app.context_processor
def inject_colab():
    def verify_coor_colab() -> Colab | None:
        """retorna a instância do colaborador, se houver"""
        colab = Colab.query.filter_by(user_id=current_user.id).first()
        return colab
    return dict(verify_coor_colab=verify_coor_colab)
        

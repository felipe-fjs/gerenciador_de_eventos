from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, event, UniqueConstraint
import datetime


def current_time():
    return datetime.datetime.now(datetime.timezone.utc)

class ColabRole(db.Model):
    __tablename__ = 'colab_roles'

    id = Column(Integer, primary_key=True)
    role = Column(String(60), nullable=False)
    created_at = Column(DateTime(), default=current_time, nullable=False)
    update_at = Column(DateTime(), default=current_time, nullable=False)


class Colab(db.Model):
    __tablename__ = 'colabs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    active = Column(Boolean(), nullable=False, default=True)


class EventColab(db.Model):
    __tablename__ = 'event_colabs'

    id = Column(Integer, primary_key=True)
    role = Column(Integer, ForeignKey('colab_roles.id'), nullable=False)
    colab_id = Column(Integer, ForeignKey('colabs.id'), nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)

    __table_args__ = (UniqueConstraint('colab_id', 'event_id', name="colab_already_in_this_event"),)


class SubEventColab(db.Model):
    __tablename__ = 'sub_event_colabs'

    id = Column(Integer, primary_key=True)
    event_colab_id = Column(Integer, ForeignKey('event_colabs.id'), nullable=False)
    sub_event_id = Column(Integer, ForeignKey('sub_events.id'), nullable=False)

    __table_args__ = (UniqueConstraint('event_colab_id', 'sub_event_id', name="colab_already_in_this_sub_event"),)


@event.listens_for(ColabRole, 'before_update')
def update_time(mapper, connection, target):
    target.update_at = current_time()

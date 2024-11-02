from app import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint


class UnciEvent(db.Model):
    """ 
        * title
        * desc
        * slug
        * start
        * end
    """
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(180), nullable=False, default="adicione um título!")
    desc = Column(Text, nullable=False, default="Descrição não adicionada!")
    slug = Column(String(60), unique=True, nullable=False)
    start = Column(DateTime(), nullable=False, default=None)
    end = Column(DateTime(), nullable=False, default=None)

    def __str__(self):
        return f"Titulo: {self.title}; \ndesc: {self.desc}; \nslug: {self.slug}; \nstart: {self.start}; \nend: {self.end}"

class SubEvent(db.Model):
    __tablename__ = 'sub_events'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(255), nullable=False, default="Título não adicionado!")
    desc = Column(Text(500), nullable=False, default="Descrição de eventos não adicionada!")
    slug = Column(String(60), unique=True, nullable=False)
    start = Column(DateTime(), nullable=False, default=None)
    end = Column(DateTime(), nullable=False, default=None)
    classroom = Column(String(20), nullable=False, default="Local de evento não atribuído!")
    
class SubEventViewer(db.Model):
    __tablename__  = 'sub_event_viewers'

    id = Column(Integer, primary_key=True)
    sub_event_id = Column(Integer, ForeignKey('sub_events.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (UniqueConstraint('sub_event_id', 'user_id', name="user_already_in_this_sub_event"),)

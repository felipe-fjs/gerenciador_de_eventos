from app import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime, event
import datetime


class UnciEvent(db.Model):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(180), nullable=False, default="adicione um título!")
    desc = Column(Text, nullable=False, default="Descrição não adicionada!")
    start = Column(DateTime(), nullable=False, default=None)
    end = Column(DateTime(), nullable=False, default=None)


class SubEvent(db.Model):
    __tablename__ = 'sub_events'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    title = Column(String(255), nullable=False, default="Título não adicionado!")
    desc = Column(String(255), nullable=False, default="Descrição de eventos não adicionada!")
    start = Column(DateTime(), nullable=False, default=None)
    end = Column(DateTime(), nullable=False, default=None)
    classroom = Column(String(20), nullable=False, default="Local de evento não atribuído!")
    
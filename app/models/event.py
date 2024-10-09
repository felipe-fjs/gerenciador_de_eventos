from app import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime, event
import datetime


class UnciEvent(db.Model):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(180), nullable=False, default="adicione um título!")
    desc = Column(Text, nullable=False, default="Descrição não adicionada!")
    
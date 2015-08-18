import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Stall(Base):
    __tablename__ = 'stall'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    status = Column(Boolean)
    visits = relationship('Visit', backref='stall')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'num_visits': len(self.visits)
        }

class Visit(Base):
    __tablename__ = 'visit'
    id = Column(Integer, primary_key=True, autoincrement=True)
    stall_id = Column(Integer, ForeignKey('stall.id'))
    entered_at = Column(DateTime, default=datetime.datetime.now)
    exited_at = Column(DateTime, default=datetime.datetime.now)

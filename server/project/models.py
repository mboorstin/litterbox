import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

EPOCH = datetime.datetime.utcfromtimestamp(0)

Base = declarative_base()

class Stall(Base):
    __tablename__ = 'stall'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address = Column(Integer)

    status = Column(Boolean)
    visits = relationship('Visit', lazy='dynamic', backref='stall')

    def to_json(self):
        last_visit = self.visits.order_by(Visit.id.desc()).first()
        live = False
        if last_visit:
            delta = datetime.datetime.now() - (last_visit.exited_at or last_visit.entered_at)
            if delta.total_seconds() < 3 * 24 * 60 * 60:
                live = True
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'status': self.status,
            'live': live,
        }

class Visit(Base):
    __tablename__ = 'visit'
    id = Column(Integer, primary_key=True, autoincrement=True)
    stall_id = Column(Integer, ForeignKey('stall.id'))
    entered_at = Column(DateTime, default=datetime.datetime.now)
    exited_at = Column(DateTime, default=EPOCH)

    def to_json(self):
        def unix_time(dt):
            delta = dt - EPOCH
            return int(delta.total_seconds())
        return {
            'id': self.id,
            'stall_id': self.stall_id,
            'entered_at': unix_time(self.entered_at),
            'exited_at': unix_time(self.exited_at),
            'duration': self.duration,
        }

    @property
    def duration(self):
        return int((self.exited_at - self.entered_at).total_seconds())


class Debug(Base):
    __tablename__ = 'debug'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    message = Column(String)

    def __str__(self):
        return '%s: %s' % (self.timestamp.isoformat(), self.message)

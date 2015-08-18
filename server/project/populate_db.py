from sqlalchemy import create_engine
from models import Stall, Visit, Base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///sqlite.db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = Session()

stalls = [
    Stall(id=1, name='berry_4_biggie', status=False),
    Stall(id=2, name='berry_4_biggie', status=False),
    Stall(id=3, name='berry_4_tuckshop', status=False),
    Stall(id=4, name='berry_4_tuckshop', status=False),
    Stall(id=5, name='berry_4_tupac', status=False),
    Stall(id=6, name='berry_4_tupac', status=False),
]
for stall in stalls:
    session.add(stall)

visits = [
    Visit(id=1, stall_id=2),
    Visit(id=2, stall_id=1),
    Visit(id=3, stall_id=4),
    Visit(id=4, stall_id=3),
    Visit(id=5, stall_id=2),
    Visit(id=6, stall_id=2),
]
for visit in visits:
    session.add(visit)

session.commit()

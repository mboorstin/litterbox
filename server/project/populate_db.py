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

session.commit()

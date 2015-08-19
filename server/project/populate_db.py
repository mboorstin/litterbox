from sqlalchemy import create_engine
from models import Stall, Visit, Base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///sqlite.db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = Session()

stalls = [
    # Address 00 13 a2 00 40 d4 a5 6d
    Stall(id=1087677805, name='berry_4_biggie', status=False),
    # Address 00 13 a2 00 40 d4 f0 28
    Stall(id=1087696936, name='berry_4_biggie', status=False),
    Stall(id=3, name='berry_4_tuckshop', status=False),
    Stall(id=4, name='berry_4_tuckshop', status=False),
    Stall(id=5, name='berry_4_tupac', status=False),
    Stall(id=6, name='berry_4_tupac', status=False),
]
for stall in stalls:
    session.add(stall)

session.commit()

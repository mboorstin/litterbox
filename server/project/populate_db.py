from sqlalchemy import create_engine
from models import Stall, Visit, Base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///sqlite.db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = Session()

stalls = [
    # ID is just the last 4 bytes in the address, leaving in base 10
    # to make it easier to know what to query from web
    # Address 0013A200 40D4A56D
    Stall(address=1087677805, name='berry_4_biggie', status=False),
    # Address 0013A200 40D4F028
    Stall(address=1087696936, name='berry_4_biggie', status=False),
    # Address 0013A200 40E82B2E
    Stall(address=1088957230, name='berry_4_tuckshop', status=False),
    # Address 0013A200 40D4EFE7
    Stall(address=1087696871, name='berry_4_tuckshop', status=False),
    # Address 0013A200 40CAE5A8
    Stall(address=1087038888, name='berry_4_tupac', status=False),
    # Address 0013A200 40E82B77
    Stall(address=1088957303, name='berry_4_tupac', status=False),
]
for stall in stalls:
    session.add(stall)

session.commit()

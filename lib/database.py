from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

def setup_database():
    engine = create_engine('sqlite:///fitness_tracker.db')
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    return DBSession, engine
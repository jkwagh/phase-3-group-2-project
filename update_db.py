# update_db.py
from sqlalchemy import create_engine
from lib.models import Base

engine = create_engine('sqlite:///fitness_tracker.db')
Base.metadata.create_all(engine)

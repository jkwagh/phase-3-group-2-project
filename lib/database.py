from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

def setup_database():
    engine = create_engine('sqlite:///fitness_tracker.db')

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session, engine

if __name__ == "__main__":
    Session, engine = setup_database()
    print("Database tables created successfully.")

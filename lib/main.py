from cli import cli
from database import setup_database
from sqlalchemy.orm import sessionmaker
from models import Base, User  # Add this line to import the User class

if __name__ == '__main__':
    DBSession, engine = setup_database()

    # Create a session
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    inspector = inspect(engine)
    for table_name in inspector.get_table_names():
        table = inspector.get_table(table_name)
        print(table)

    # Add sample data
    user1 = User(name='John Doe', age=30, fitness_goals='Lose weight')
    session.add(user1)
    session.commit()

    # Start the CLI
    cli()

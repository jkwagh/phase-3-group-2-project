import click
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from models import Base, User, Workout, Exercise
from database import setup_database

DBSession, engine = setup_database()

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@click.group()
def cli():
    """Fitness Tracker CLI"""

@cli.command()
@click.option('--name', prompt='Enter the user name', help='User name')
@click.option('--age', prompt='Enter the age', type=int, help='User age')
@click.option('--fitness_goals', prompt='Enter fitness goals', help='User fitness goals')
def create_user(name, age, fitness_goals):
    """Create a new user"""
    user = User.create(session, name=name, age=age, fitness_goals=fitness_goals)
    click.echo(f"User {name} created successfully with ID: {user.id}")

@cli.command()
@click.option('--user_id', prompt='Enter the user ID to delete', type=int, help='User ID to delete')
def delete_user(user_id):
    """Delete a user"""
    User.delete(session, user_id)
    click.echo(f"User with ID {user_id} deleted successfully!")

@cli.command()
@click.option('--user_id', prompt='Enter the user ID', type=int, help='User ID')
@click.option('--date', prompt='Enter the date (YYYY-MM-DD)', help='Workout date')
@click.option('--duration', prompt='Enter the duration in minutes', type=int, help='Workout duration')
def add_workout(user_id, date, duration):
    """Add a workout"""
    workout = Workout.create(session, date=datetime.strptime(date, '%Y-%m-%d'), duration=duration, user_id=user_id)
    click.echo(f"Workout logged for user ID {user_id} on {date} for {duration} minutes with ID: {workout.id}")

@cli.command()
@click.option('--workout_id', prompt='Enter the workout ID to delete', type=int, help='Workout ID to delete')
def delete_workout(workout_id):
    """Delete a workout"""
    Workout.delete(session, workout_id)
    click.echo(f"Workout with ID {workout_id} deleted successfully!")

@cli.command()
def display_users():
    """Display all users"""
    users = User.get_all(session)
    for user in users:
        click.echo(f"User ID: {user.id}, Name: {user.name}, Age: {user.age}, Fitness Goals: {user.fitness_goals}")

@cli.command()
def display_workouts():
    """Display all workouts"""
    workouts = Workout.get_all(session)
    for workout in workouts:
        click.echo(f"Workout ID: {workout.id}, Date: {workout.date}, Duration: {workout.duration} minutes")

@cli.command()
def display_exercises():
    """Display all exercises"""
    exercises = Exercise.get_all(session)
    for exercise in exercises:
        click.echo(f"Exercise ID: {exercise.id}, Name: {exercise.name}, Type: {exercise.type}, Difficulty: {exercise.difficulty}")

@cli.command()
@click.option('--user_id', prompt='Enter the user ID to find', type=int, help='User ID to find')
def find_user(user_id):
    """Find user by ID"""
    user = User.find_by_id(session, user_id)
    if user:
        click.echo(f"User ID: {user.id}, Name: {user.name}, Age: {user.age}, Fitness Goals: {user.fitness_goals}")
    else:
        click.echo(f"User with ID {user_id} not found.")

@cli.command()
@click.option('--workout_id', prompt='Enter the workout ID to find', type=int, help='Workout ID to find')
def find_workout(workout_id):
    """Find workout by ID"""
    workout = Workout.find_by_id(session, workout_id)
    if workout:
        click.echo(f"Workout ID: {workout.id}, Date: {workout.date}, Duration: {workout.duration} minutes")
    else:
        click.echo(f"Workout with ID {workout_id} not found.")

@cli.command()
@click.option('--exercise_id', prompt='Enter the exercise ID to find', type=int, help='Exercise ID to find')
def find_exercise(exercise_id):
    """Find exercise by ID"""
    exercise = Exercise.find_by_id(session, exercise_id)
    if exercise:
        click.echo(f"Exercise ID: {exercise.id}, Name: {exercise.name}, Type: {exercise.type}, Difficulty: {exercise.difficulty}")
    else:
        click.echo(f"Exercise with ID {exercise_id} not found.")

if __name__ == '__main__':
    cli()
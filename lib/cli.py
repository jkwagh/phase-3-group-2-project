import click
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from models import Base, User, Workout, Exercise
from database import setup_database

DBSession, engine = setup_database()

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def validate_positive_integer(value, field_name):
    if value <= 0:
        raise ValueError(f"{field_name} must be a positive integer.")

def validate_date_format(value):
    try:
        return datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

@click.group()
def cli():
    """Fitness Tracker CLI"""

@cli.command()
@click.option('--name', prompt='Enter the user name', help='User name')
@click.option('--age', prompt='Enter the age', type=int, help='User age')
@click.option('--fitness_goals', prompt='Enter fitness goals', help='User fitness goals')
def create_user(name, age, fitness_goals):
    """Create a new user"""
    try:
        user = User.create(session, name=name, age=age, fitness_goals=fitness_goals)
        click.echo(f"User {name} created successfully with ID: {user.id}")
    except Exception as e:
        click.echo(f"Error creating user: {e}")

@cli.command()
@click.option('--user_id', prompt='Enter the user ID to delete', type=int, help='User ID to delete')
def delete_user(user_id):
    """Delete a user"""
    try:
        User.delete(session, user_id)
        click.echo(f"User with ID {user_id} deleted successfully!")
    except Exception as e:
        click.echo(f"Error deleting user: {e}")

@cli.command()
@click.option('--user_id', prompt='Enter the user ID', type=int, help='User ID')
@click.option('--date', prompt='Enter the date (YYYY-MM-DD)', help='Workout date')
@click.option('--duration', prompt='Enter the duration in minutes', type=int, help='Workout duration')
def add_workout(user_id, date, duration):
    """Add a workout"""
    try:
        date_obj = validate_date_format(date)
        validate_positive_integer(duration, "Duration")
        workout = Workout.create(session, date=date_obj, duration=duration, user_id=user_id)
        click.echo(f"Workout logged for user ID {user_id} on {date} for {duration} minutes with ID: {workout.id}")
    except ValueError as ve:
        click.echo(f"Error: {ve}")
    except Exception as e:
        click.echo(f"Error adding workout: {e}")

@cli.command()
@click.option('--workout_id', prompt='Enter the workout ID to delete', type=int, help='Workout ID to delete')
def delete_workout(workout_id):
    """Delete a workout"""
    try:
        Workout.delete(session, workout_id)
        click.echo(f"Workout with ID {workout_id} deleted successfully!")
    except Exception as e:
        click.echo(f"Error deleting workout: {e}")
        
@cli.command()
def display_users():
    """Display all users"""
    try:
        users = User.get_all(session)
        for user in users:
            click.echo(f"User ID: {user.id}, Name: {user.name}, Age: {user.age}, Fitness Goals: {user.fitness_goals}")
    except Exception as e:
        click.echo(f"Error displaying users: {e}")

@cli.command()
def display_workouts():
    """Display all workouts"""
    try:
        workouts = Workout.get_all(session)
        for workout in workouts:
            click.echo(f"Workout ID: {workout.id}, Date: {workout.date}, Duration: {workout.duration} minutes")
    except Exception as e:
        click.echo(f"Error displaying workouts: {e}")

@cli.command()
def display_exercises():
    """Display all exercises"""
    try:
        exercises = Exercise.get_all(session)
        for exercise in exercises:
            click.echo(f"Exercise ID: {exercise.id}, Name: {exercise.name}, Type: {exercise.type}, Difficulty: {exercise.difficulty}")
    except Exception as e:
        click.echo(f"Error displaying exercises: {e}")

@cli.command()
@click.option('--user_id', prompt='Enter the user ID to find', type=int, help='User ID to find')
def find_user(user_id):
    """Find user by ID"""
    try:
        user = User.find_by_id(session, user_id)
        if user:
            click.echo(f"User ID: {user.id}, Name: {user.name}, Age: {user.age}, Fitness Goals: {user.fitness_goals}")
        else:
            click.echo(f"User with ID {user_id} not found.")
    except Exception as e:
        click.echo(f"Error finding user: {e}")

@cli.command()
@click.option('--workout_id', prompt='Enter the workout ID to find', type=int, help='Workout ID to find')
def find_workout(workout_id):
    """Find workout by ID"""
    try:
        workout = Workout.find_by_id(session, workout_id)
        if workout:
            click.echo(f"Workout ID: {workout.id}, Date: {workout.date}, Duration: {workout.duration} minutes")
        else:
            click.echo(f"Workout with ID {workout_id} not found.")
    except Exception as e:
        click.echo(f"Error finding workout: {e}")

@cli.command()
@click.option('--exercise_id', prompt='Enter the exercise ID to find', type=int, help='Exercise ID to find')
def find_exercise(exercise_id):
    """Find exercise by ID"""
    try:
        exercise = Exercise.find_by_id(session, exercise_id)
        if exercise:
            click.echo(f"Exercise ID: {exercise.id}, Name: {exercise.name}, Type: {exercise.type}, Difficulty: {exercise.difficulty}")
        else:
            click.echo(f"Exercise with ID {exercise_id} not found.")
    except Exception as e:
        click.echo(f"Error finding exercise: {e}")

@cli.command()
@click.option('--name', prompt='Enter the exercise name', help='Exercise name')
@click.option('--type', prompt='Enter the exercise type', help='Exercise type')
@click.option('--difficulty', prompt='Enter the exercise difficulty', type=int, help='Exercise difficulty')
@click.option('--sets', prompt='Enter the number of sets', type=int, help='Number of sets')
@click.option('--reps', prompt='Enter the number of reps', type=int, help='Number of reps')
def add_exercise(name, type, difficulty, sets, reps):
    """Add a new exercise"""
    try:
        validate_positive_integer(difficulty, "Difficulty")
        validate_positive_integer(sets, "Number of sets")
        validate_positive_integer(reps, "Number of reps")

        exercise = Exercise.create(session, name=name, exercise_type=type, difficulty=difficulty, sets=sets, reps=reps)
        click.echo(f"Exercise {name} added successfully with ID: {exercise.id}")
    except ValueError as ve:
        click.echo(f"Error: {ve}")
    except Exception as e:
        click.echo(f"Error adding exercise: {e}")

@cli.command()
@click.option('--exercise_id', prompt='Enter the exercise ID to delete', type=int, help='Exercise ID to delete')
def delete_exercise(exercise_id):
    """Delete an exercise"""
    try:
        Exercise.delete(session, exercise_id)
        click.echo(f"Exercise with ID {exercise_id} deleted successfully!")
    except Exception as e:
        click.echo(f"Error deleting exercise: {e}")

if __name__ == '__main__':
    cli()

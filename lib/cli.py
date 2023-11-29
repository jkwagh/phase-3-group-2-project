import click
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from models import Base, User, Workout, Exercise
from database import setup_database

# Call setup_database to get the engine
DBSession, engine = setup_database()

# Create a session
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@click.group()
def cli():
    """Fitness Tracker CLI"""

@cli.command()
@click.option('--name', prompt='Enter your name', help='Your name')
@click.option('--age', prompt='Enter your age', type=int, help='Your age')
@click.option('--fitness_goals', prompt='Enter your fitness goals', help='Your fitness goals')
def create_user(name, age, fitness_goals):
    """Create a new user"""
    user = User(name=name, age=age, fitness_goals=fitness_goals)
    session.add(user)
    session.commit()
    click.echo(f"User {name} created successfully with ID: {user.id}")

@cli.command()
@click.option('--user_id', prompt='Enter your user ID', type=int, help='Your user ID')
@click.option('--date', prompt='Enter the date (YYYY-MM-DD)', help='Workout date')
@click.option('--duration', prompt='Enter the duration in minutes', type=int, help='Workout duration')
def log_workout(user_id, date, duration):
    """Log a workout"""
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        click.echo(f"User with ID {user_id} not found.")
        return

    workout = Workout(date=datetime.strptime(date, '%Y-%m-%d'), duration=duration, user=user)
    session.add(workout)
    session.commit()

    click.echo(f"Workout logged for {user.name} on {date} for {duration} minutes.")

@cli.command()
def view_workouts():
    """View all workouts"""
    workouts = session.query(Workout).all()
    for workout in workouts:
        click.echo(f"Workout ID: {workout.id}, Date: {workout.date}, Duration: {workout.duration} minutes")

@cli.command()
@click.option('--workout_id', prompt='Enter the workout ID to delete', type=int, help='Workout ID to delete')
def delete_workout(workout_id):
    """Delete a workout"""
    workout = session.query(Workout).filter_by(id=workout_id).first()
    if not workout:
        click.echo(f"Workout with ID {workout_id} not found.")
        return

    session.delete(workout)
    session.commit()
    click.echo(f"Workout with ID {workout_id} deleted successfully!")

@cli.command()
def add_exercise():
    # Command to add an exercise
    name = click.prompt("Enter exercise name", type=str)
    type = click.prompt("Enter exercise type", type=str)
    difficulty = click.prompt("Enter exercise difficulty", type=str)
    sets = click.prompt("Enter number of sets", type=int)
    reps = click.prompt("Enter number of reps", type=int)

    exercise = Exercise(name=name, type=type, difficulty=difficulty, sets=sets, reps=reps)
    session.add(exercise)
    session.commit()

    click.echo("Exercise added successfully!")

@cli.command()
def delete_exercise():
    # Command to delete an exercise
    exercise_id = click.prompt("Enter exercise ID to delete", type=int)

    exercise = session.query(Exercise).get(exercise_id)
    if exercise:
        session.delete(exercise)
        session.commit()
        click.echo("Exercise deleted successfully!")
    else:
        click.echo("Exercise not found.")

@cli.command()
def add_exercise_to_workout():
    # Command to add an exercise to a workout
    workout_id = click.prompt("Enter workout ID", type=int)
    exercise_id = click.prompt("Enter exercise ID to add to the workout", type=int)

    workout = session.query(Workout).get(workout_id)
    exercise = session.query(Exercise).get(exercise_id)

    if workout and exercise:
        workout.exercises.append(exercise)
        session.commit()
        click.echo("Exercise added to the workout successfully!")
    else:
        click.echo("Workout or exercise not found.")

@cli.command()
def delete_exercise_from_workout():
    # Command to delete an exercise from a workout
    workout_id = click.prompt("Enter workout ID", type=int)
    exercise_id = click.prompt("Enter exercise ID to delete from the workout", type=int)

    workout = session.query(Workout).get(workout_id)
    exercise = session.query(Exercise).get(exercise_id)

    if workout and exercise:
        workout.exercises.remove(exercise)
        session.commit()
        click.echo("Exercise deleted from the workout successfully!")
    else:
        click.echo("Workout or exercise not found.")

@cli.command()
@click.option('--user_id', prompt='Enter your user ID', type=int, help='Your user ID')
def analyze_workout_history(user_id):
    """Analyze workout history for a user"""
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        click.echo(f"User with ID {user_id} not found.")
        return

    click.echo(f"Workout history for {user.name}:")
    for workout in user.workouts:
        click.echo(f"Workout ID: {workout.id}, Date: {workout.date}, Duration: {workout.duration} minutes")

if __name__ == '__main__':
    cli()

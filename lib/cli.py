import click
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from models import Base, User, Workout, Exercise, WorkoutExercises
from database import setup_database
from prettytable import PrettyTable
import pyfiglet
import time
import random

DBSession, engine = setup_database()

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

quotes = [
    "Workout more so you can eat more donuts",
    "If you've got 99 problems, go to the gym to ignore all of them",
    "I want to see what happens if I don't give up",
    "You must exercise in the morning before your brain figures out what you're doing",
    "PROTEIN,PROTEIN, PROTEIN, PROTEIN, PROTEIN, PROTEIN, PROTEIN",
]

def display_progress_bar():
    with click.progressbar(range(10), label='Creating User') as bar:
        for _ in bar:
            time.sleep(0.1)

def display_random_quote():
    random_quote = random.choice(quotes)
    colors = ['blue', 'magenta', 'cyan', 'white']
    random_color = random.choice(colors)
    styled_quote = click.style(random_quote, italic=True, fg=random_color)
    click.echo(f"Gym Gods Tips (GGT): {styled_quote}")

def validate_positive_integer(value, field_name):
    if value <= 0:
        raise ValueError(click.style(f"{field_name} must be a positive integer.", fg='red'))

def validate_date_format(value):
    try:
        return datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        raise ValueError(click.style("Invalid date format. Please use YYYY-MM-DD.", fg='red'))

def display_users_table(users):
    table = PrettyTable()
    table.field_names = ["ID", "Name", "Age", "Fitness Goals"]
    for user in users:
        table.add_row([user.id, user.name, user.age, user.fitness_goals])
    click.echo(table)

def display_workouts_table(workouts):
    table = PrettyTable()
    table.field_names = ["ID", "Date", "Duration", "User ID"]
    for workout in workouts:
        table.add_row([workout.id, workout.date, workout.duration, workout.user_id])
    click.echo(table)

def display_exercises_table(exercises):
    table = PrettyTable()
    table.field_names = ["ID", "Name", "Type", "Difficulty", "Sets", "Reps"]
    for exercise in exercises:
        table.add_row([exercise.id, exercise.name, exercise.type, exercise.difficulty, exercise.sets, exercise.reps])
    click.echo(table)

@click.group()
def cli():
    """Fitness Tracker CLI"""
    f = pyfiglet.Figlet(font="slant")
    title_art = f.renderText('Time to get fit!')
    colored_title = click.style(title_art, fg='green')
    print(colored_title)

@cli.command()
@click.option('--name', prompt='Enter the user name', help='User name')
@click.option('--age', prompt='Enter the age', type=int, help='User age')
@click.option('--fitness_goals', prompt='Enter fitness goals', help='User fitness goals')
def create_user(name, age, fitness_goals):
    """Create a new user"""
    try:
        with click.progressbar(range(10), label='Creating User') as bar:
            for _ in bar:
                time.sleep(0.1)
        click.clear()
        click.echo("Creating User...")
        display_random_quote()
        user = User.create(session, name=name, age=age, fitness_goals=fitness_goals)
        click.echo(click.style(f"User {name} created successfully with ID: {user.id}", fg='green'))
    except Exception as e:
        click.echo(click.style(f"Error creating user: {e}", fg='red'))

@cli.command()
@click.option('--user_id', prompt='Enter the user ID to delete', type=int, help='User ID to delete')
def delete_user(user_id):
    """Delete a user"""
    try:
        User.delete(session, user_id)
        click.echo(click.style(f"User with ID {user_id} deleted successfully!", fg= 'green'))
    except Exception as e:
        click.echo(click.style(f"Error deleting user: {e}", fg= 'red'))

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

        click.echo(f"Add exercises to the workout (type 'done' when finished):")

        while True:
            exercise_name = click.prompt('Enter exercise name (or type "done" to finish adding exercises)', default="done")

            if exercise_name.lower() == "done":
                break

            exercise_type = click.prompt('Enter exercise type')
            exercise_difficulty = click.prompt('Enter exercise difficulty', type=int)
            exercise_sets = click.prompt('Enter the number of sets', type=int)
            exercise_reps = click.prompt('Enter the number of reps', type=int)

            exercise = Exercise.create(session, name=exercise_name, exercise_type=exercise_type, difficulty=exercise_difficulty, sets=exercise_sets, reps=exercise_reps)
            WorkoutExercises.create(session, workout_id=workout.id, exercise_id=exercise.id, sets_completed=exercise_sets, reps_completed=exercise_reps)

        with click.progressbar(range(10), label='Creating Workout') as bar:
            for _ in bar:
                time.sleep(0.1)
        click.clear()
        click.echo("Creating Workout...")

        click.echo(click.style(f"Workout logged for user ID {user_id} on {date} for {duration} minutes with ID: {workout.id}", fg='green'))
    except ValueError as ve:
        click.echo(f"Error: {ve}")
    except Exception as e:
        click.echo(click.style(f"Error adding workout: {e}", fg='red'))


@cli.command()
@click.option('--workout_id', prompt='Enter the workout ID to delete', type=int, help='Workout ID to delete')
def delete_workout(workout_id):
    """Delete a workout"""
    try:
        Workout.delete(session, workout_id)
        click.echo(click.style(f"Workout with ID {workout_id} deleted successfully!", fg= 'green'))
    except Exception as e:
        click.echo(f"Error deleting workout: {e}")
        
@cli.command()
def display_users():
    """Display all users"""
    try:
        users = User.get_all(session)
        display_users_table(users)
    except Exception as e:
        click.echo(f"Error displaying users: {e}")

@cli.command()
def display_workouts():
    """Display all workouts"""
    try:
        workouts = Workout.get_all(session)
        display_workouts_table(workouts)
    except Exception as e:
        click.echo(f"Error displaying workouts: {e}")

@cli.command()
def display_exercises():
    """Display all exercises"""
    try:
        exercises = Exercise.get_all(session)
        display_exercises_table(exercises)
    except Exception as e:
        click.echo(f"Error displaying exercises: {e}")

@cli.command()
@click.option('--user_id', prompt='Enter the user ID to find', type=int, help='User ID to find')
def find_user(user_id):
    """Find user by ID"""
    try:
        user = User.find_by_id(session, user_id)
        if user:
            click.echo(click.style(f"User ID: {user.id}, Name: {user.name}, Age: {user.age}, Fitness Goals: {user.fitness_goals}", fg = 'green'))
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
            click.echo(click.style(f"Workout ID: {workout.id}, Date: {workout.date}, Duration: {workout.duration} minutes", fg = 'green'))
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
            click.echo(click.style(f"Exercise ID: {exercise.id}, Name: {exercise.name}, Type: {exercise.type}, Difficulty: {exercise.difficulty}", fg= 'green'))
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
        click.echo(click.style(f"Exercise {name} added successfully with ID: {exercise.id}", fg= 'green'))
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
        click.echo(click.style(f"Exercise with ID {exercise_id} deleted successfully!", fg='green'))

    except Exception as e:
        click.echo(f"Error deleting exercise: {e}")

if __name__ == '__main__':
    cli()

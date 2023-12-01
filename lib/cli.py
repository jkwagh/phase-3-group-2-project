import click
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
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

current_user = None

quotes = [
   "Be stronger than your excuse: Determination is stronger than any excuse.",
    "Progress and perfection: Strive for progress, not perfection.",
    "Work in progress: Always proud of making progress.",
    "Motivation will get you started, habits will keep you going",
    "The hard days are the best because that's when champions are made",
    "A true gym rat wouldn't dream of stopping until they've given their all",
    "Success usually comes to those who are too busy to be looking for it",
    "Sweat, sacrifice, success",
    "Every rep counts, every effort matters",
    "My body is my machine",
    "Pushing through the pain, embracing the gain",
    "No shortcuts, just hard work & determination",
    "Crushing goals, one workout at a time"
]

def display_progress_bar():
    with click.progressbar(range(10), label='Creating User') as bar:
        for _ in bar:
            time.sleep(0.1)

def display_random_quote():
    random_quote = random.choice(quotes)
    colors = ['blue', 'cyan']
    random_color = random.choice(colors)
    styled_quote = click.style(random_quote, italic=True, fg=random_color)
    click.echo(f"Gym Gods Tips (GGT): {styled_quote}")

def validate_positive_integer(value, field_name):
    if value <= 0:
        raise ValueError(click.style(f"{field_name} must be a positive integer.", fg='red'))

def validate_date_format(value):
    try:
        return datetime.strptime(value, '%m-%d-%Y')
    except ValueError:
        raise ValueError(click.style("Invalid date format. Please use MM-DD-YYYY.", fg='red'))

def display_users_table(users):
    table = PrettyTable()
    table.field_names = ["ID", "Name", "Age", "Fitness Goals"]
    for user in users:
        table.add_row([user.id, user.name, user.age, user.fitness_goals])
    click.echo(table)
    return_to_main_menu = click.confirm("Do you want to return to the Main Menu?", default=True)
    if return_to_main_menu:
        main_menu()

def display_workouts_table(workouts):
    table = PrettyTable()
    table.field_names = ["ID", "Date", "Duration", "User ID"]
    for workout in workouts:
        formatted_date = workout.date.strftime('%B %d, %Y')
        table.add_row([workout.id, formatted_date, workout.duration, workout.user_id])
    click.echo(table)

def display_exercises_table(exercises):
    table = PrettyTable()
    table.field_names = ["ID", "Name", "Type", "Difficulty", "Sets", "Reps"]
    for exercise in exercises:
        table.add_row([exercise.id, exercise.name, exercise.type, exercise.difficulty, exercise.sets, exercise.reps])
    click.echo(table)

def display_title():
    f = pyfiglet.Figlet(font="slant")
    title_art = f.renderText('Time to get fit!')
    colored_title = click.style(title_art, fg='green')
    click.echo(colored_title)

@click.group()
def cli():
    """Fitness Tracker CLI"""
    display_title()

@cli.command()
@click.option('--username', prompt='Enter the username', help='Username', required=True)
@click.option('--password', prompt='Enter the password', hide_input=True, confirmation_prompt=True)
@click.option('--name', prompt='Enter your name', help='User name')
@click.option('--age', prompt='Enter your age', type=int, help='User age')
@click.option('--fitness_goals', prompt='Enter your fitness goals', help='User fitness goals')
def create_user(username, password, name, age, fitness_goals):
    """Create a new user"""
    try:
        with click.progressbar(range(10), label='Creating User') as bar:
            for _ in bar:
                time.sleep(0.1)
        click.clear()
        click.echo("Creating User...")
        display_random_quote()
        user = User.create(session, username=username, password=password, name=name, age=age, fitness_goals=fitness_goals)
        click.echo(click.style(f"User {username} created successfully with ID: {user.id}", fg='green'))
    except Exception as e:
        click.echo(click.style(f"Error creating user: {e}", fg='red'))
    return_to_main_menu = click.confirm("Do you want to return to the Main Menu?", default=True)
    if return_to_main_menu:
        main_menu()

@cli.command()
@click.option('--user_id', prompt='Enter the user ID to delete', type=int, help='User ID to delete')
def delete_user(user_id):
    """Delete a user by ID"""
    try:
        User.delete(session, user_id)
        click.echo(click.style(f"User with ID {user_id} deleted successfully!", fg='green'))
    except Exception as e:
        click.echo(click.style(f"Error deleting user: {e}", fg='red'))

    return_to_main_menu = click.confirm("Do you want to return to the Main Menu?", default=True)
    if return_to_main_menu:
        main_menu()

@cli.command()
def add_workout():
    """Add a workout"""
    global current_user
    if current_user is None:
        click.echo(click.style("Please log in first.", fg='red'))
        return

    while True:
        try:
            date = click.prompt('Enter workout date (MM-DD-YYYY)')
            duration = click.prompt('Enter workout duration in minutes', type=int)
            date_obj = validate_date_format(date)
            validate_positive_integer(duration, "Duration")
            workout = Workout.create(session, date=date_obj, duration=duration, user_id=current_user.id)

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

            click.echo(click.style(f"Workout logged for user ID {current_user.id} on {date} for {duration} minutes with ID: {workout.id}", fg='green'))

            return_to_user_menu = click.confirm("Do you want to return to the User Menu?", default=True)
            if return_to_user_menu:
                user_menu()

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
    return_to_user_menu = click.confirm("Do you want to return to the User Menu?", default=True)
    if return_to_user_menu:
        user_menu()
        
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
    return_to_user_menu = click.confirm("Do you want to return to the User Menu?", default=True)
    if return_to_user_menu:
        user_menu()

@cli.command()
def display_exercises():
    """Display all exercises"""
    try:
        exercises = Exercise.get_all(session)
        display_exercises_table(exercises)
    except Exception as e:
        click.echo(f"Error displaying exercises: {e}")
    return_to_user_menu = click.confirm("Do you want to return to the User Menu?", default=True)
    if return_to_user_menu:
        user_menu()
@cli.command()
def find_user():
    """Find the logged-in user"""
    global current_user
    if current_user is None:
        click.echo(click.style("Please log in first.", fg='red'))
    else:
        click.echo(click.style(f"Logged-in user: {current_user.username}", fg='green'))

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
    return_to_user_menu = click.confirm("Do you want to return to the User Menu?", default=True)
    if return_to_user_menu:
        user_menu()

@cli.command()
@click.option('--exercise_id', prompt='Enter the exercise ID to delete', type=int, help='Exercise ID to delete')
def delete_exercise(exercise_id):
    """Delete an exercise"""
    try:
        Exercise.delete(session, exercise_id)
        click.echo(click.style(f"Exercise with ID {exercise_id} deleted successfully!", fg='green'))

    except Exception as e:
        click.echo(f"Error deleting exercise: {e}")
    return_to_user_menu = click.confirm("Do you want to return to the User Menu?", default=True)
    if return_to_user_menu:
        user_menu()

@cli.command()
@click.option('--workout_id', prompt='Enter the workout ID to find', type=int, help='Workout ID to find')
def find_workout_exercises(workout_id):
    """Display exercises associated with workouts"""
    try:
        workout = Workout.find_by_id(session, workout_id)
        if workout:
            click.echo(click.style(f"Workout ID: {workout.id}, Date: {workout.date}, Duration: {workout.duration} minutes", fg='green'))

            exercises = session.query(Exercise).join(WorkoutExercises).filter(WorkoutExercises.workout_id == workout.id).all()

            if exercises:
                click.echo("Exercises:")
                for exercise in exercises:
                    click.echo(click.style(f"- ID: {exercise.id}, Name: {exercise.name}, Type: {exercise.type}, Difficulty: {exercise.difficulty}", fg='blue'))
            else:
                click.echo("No exercises found for this workout.")
        else:
            click.echo(f"Workout with ID {workout_id} not found.")
    except Exception as e:
        click.echo(f"Error finding workout: {e}")
    return_to_user_menu = click.confirm("Do you want to return to the User Menu?", default=True)
    if return_to_user_menu:
        user_menu()
@cli.command()
def logout():
    """Log out the current user"""
    global current_user
    current_user = None
    click.echo(click.style("Successfully logged out.", fg='green'))

def display_user_menu_ascii_art():
    user_menu_art = """
⠀  ⠀   (\\__/)
       (•ㅅ•)      It's time
    ＿ノヽ ノ＼＿      to hit
`/　`/ ⌒Ｙ⌒ Ｙ  ヽ     the gym.
( 　(三ヽ人　 /　  |
|　ﾉ⌒＼ ￣￣ヽ   ノ
ヽ＿＿＿＞､＿_／
       ｜( 王 ﾉ〈  (\\__/)
       /ﾐ`ー―彡\\  (•ㅅ•)
      / ╰    ╯ \\/     \\>
"""
    click.echo(user_menu_art)


def user_menu():
    """Menu for logged-in users"""
    display_user_menu_ascii_art()
    while True:
        click.echo(click.style("User Menu:", fg='green'))
        click.echo("1. Add Workout")
        click.echo("2. Delete Workout")
        click.echo("3. Display Workouts")
        click.echo("4. Add Exercise")
        click.echo("5. Delete Exercise")
        click.echo("6. Display Exercises")
        click.echo("7. Show Exercises in Workout")
        click.echo("8. Logout")

        choice = click.prompt("Enter your choice (1-8)", type=int)

        if choice == 1:
            add_workout()
        elif choice == 2:
            delete_workout()
        elif choice == 3:
            display_workouts()
        elif choice == 4:
            add_exercise()
        elif choice == 5:
            delete_exercise()
        elif choice == 6:
            display_exercises()
        elif choice == 7:
            find_workout_exercises()
        elif choice == 8:
            logout()
            break  
        else:
            click.echo("Invalid choice. Please enter a number between 1 and 8.")

@cli.command()
@click.option('--username', prompt='Enter the username', help='Username')
@click.option('--password', prompt='Enter the password', hide_input=True)
def login(username, password):
    """Log in as an existing user"""
    global current_user
    user = User.get_by_username(session, username)
    if user and user.check_password(password):
        current_user = user  
        click.echo(click.style(f"Successfully logged in as {username}", fg='green'))
        user_menu()
    else:
        click.echo(click.style("Invalid username or password", fg='red'))
    return_to_main_menu = click.confirm("Do you want to return to the Main Menu?", default=True)
    if return_to_main_menu:
        main_menu()
SESSION_FILE = "user_session.txt"

def save_session(username):
    """Save user session information to a file"""
    with open(SESSION_FILE, 'w') as file:
        file.write(username)

def load_session():
    """Load user session information from a file"""
    try:
        with open(SESSION_FILE, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

@cli.command()
@click.option('--username', prompt='Enter the username to delete', help='Username to delete')
def delete_user_by_username(username):
    """Delete a user by username"""
    try:
        user = User.get_by_username(session, username)
        if user:
            User.delete(session, user.id)
            click.echo(click.style(f"User with username {username} deleted successfully!", fg='green'))
        else:
            click.echo(f"User with username {username} not found.")
    except Exception as e:
        click.echo(f"Error deleting user: {e}")

    return_to_main_menu = click.confirm("Do you want to return to the Main Menu?", default=True)
    if return_to_main_menu:
        main_menu()


def display_main_menu_ascii_art():
    main_menu_art = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⢤⡖⠺⠉⠓⠢⣄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⢞⣿⣿⣭⣟⣯⣾⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⢸⣅⠉⠀⢻⣦⠀⡀⠘⣆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣟⣿⡿⣿⣿⣿⢟⣿⣿⠟⢿⡀⠀⠀⠀⠀⠀⠀⠀⢟⣿⣾⣿⣿⣿⣇⠀⢡⠘⣆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣶⣿⣻⡿⠁⠀⠀⢣⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠉⠉⠁⢻⠈⡆⢳⡈⢳⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⢿⣿⣿⣿⣿⣽⣿⡏⠀⠐⠾⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠟⢰⡥⠀⢝⣄⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣷⡘⠃⠀⠀⠀⠀⠙⢁⣱⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢼⢣⠞⣀⢇⠈⠱⠚⣆⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⢿⣻⣿⣿⣿⡅⠀⠀⠀⢦⣬⡇⠀⠀⠀⠀⠀⠀⠀⢠⠚⡏⠉⠑⢺⡄⠀⠀⠙⣧⡀⠇⠀⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⣷⠈⠉⠙⠛⠿⢿⣷⣦⣄⢰⣾⠖⣊⣉⡩⠍⢉⠓⠶⣿⢁⠜⢇⠁⢀⣹⣷⣤⣤⣈⣇⠀⣸⢧
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⢛⡇⠉⠀⠀⡀⢀⡀⠀⠀⠉⢙⡏⠁⠀⢹⣇⡀⠙⣏⠢⡌⡉⠉⣒⡷⠚⠉⠉⢻⣿⣿⣿⣵⣾⣷⣾
⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠚⠁⢀⣼⠋⣿⡅⠀⠀⠀⠀⠈⠉⠓⣦⡨⠀⡀⠀⠀⢈⣉⡒⠒⣶⡶⠂⠉⠀⠠⣤⣴⣶⣾⣿⣿⠿⠛⠉⠁
⠀⠀⠀⠀⠀⠀⠀⣴⠋⠉⠙⠋⠉⢸⣥⡤⠜⠋⢤⣦⢤⣤⣴⡾⠟⠁⠀⠙⢒⣫⣥⣴⣶⣿⣏⠀⠉⠛⠿⢿⣿⣿⣿⡿⠋⠁⠀⠀⠀⠀
⠀⠀⠀⠀⢀⡤⠚⠙⣷⣿⣦⡀⠀⢨⡏⠀⠀⠀⠀⠀⠀⠀⣩⠀⠀⠀⠉⠉⠉⢉⡛⢻⣿⣿⣿⣷⣶⣶⣶⣶⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣰⠏⢀⠀⠀⣖⠈⠁⠉⠙⢻⣷⣄⣀⣤⣤⡴⠿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡏⢰⡟⠀⠀⣿⡄⠀⠀⠀⣿⠀⠀⠀⠀⠀⢀⣴⠟⠁⢿⣄⣀⡀⠀⣀⣤⣶⣿⣿⣾⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣸⠀⢸⡁⠀⠀⠸⣿⣄⠀⡀⣿⠀⠀⡠⣶⡷⠋⡀⠀⠀⠚⠛⠛⠛⠛⠛⠛⠃⠈⠑⡿⢸⣯⡝⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢠⠇⠀⠘⣿⣦⣤⣤⣿⡟⠛⠓⢿⣞⠻⠟⣔⠲⡇⣀⡀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⢠⣾⣺⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⠀⠀⠀⣿⣿⠉⠛⠿⢦⣄⡠⠘⡆⣀⣤⠀⠀⠀⢐⣮⠗⠃⠋⠛⠛⠛⠛⠛⢻⣿⡿⡍⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣼⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠭⠌⣧⢾⣧⣤⣾⣦⠥⢠⣀⣀⢄⣠⣦⣶⣾⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⠀⣀⣴⣿⣿⣿⣿⣦⡂⠀⠀⠀⣾⣙⡇⠀⠀⠀⠀⠀⠀⠁⠀⣡⣿⣿⣿⣿⣯⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⡿⢋⣡⣾⣿⣿⣟⣻⠿⣿⠷⣤⣿⣿⣇⠀⠀⠀⠀⠀⠠⣀⣿⣿⣿⠛⠛⠻⠏⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢰⡟⣻⣿⣿⣿⣿⣿⣼⡏⠀⠈⠑⢤⣹⡿⣿⣯⠻⢿⣿⣿⣿⣽⠿⢟⣃⣀⣀⡨⣏⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣾⣾⠁⠀⠈⢹⣿⣿⠟⠀⠀⠀⠀⠀⠈⠛⢾⣿⡆⣶⣿⣿⠗⠒⢉⣉⣉⣙⣛⢿⣧⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢹⣿⠀⠀⢷⡀⢻⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣷⣿⣿⣷⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠈⠿⣄⠀⣸⣿⣄⣻⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣏⣉⣉⣉⣉⣉⣿⣏⣉⣉⣉⣉⣉⣉⣙⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠙⢷⣌⠧⠈⡇⠀⠀⠀⠀⠀⠀⠀⠀⢠⡟⣟⣏⣿⣷⡇⢸⣿⣿⣿⣿⣿⠆⣿⠀⠿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """
    click.echo(main_menu_art)

@cli.command()
def main_menu():
    """Main menu for the Fitness Tracker"""
    display_title()
    time.sleep(1)  
    click.clear() 

    display_main_menu_ascii_art()
    time.sleep(1)  
    click.clear() 

    display_title()
    time.sleep(1)
    
    global current_user
    while True:
        click.echo(click.style("Main Menu:", fg='green'))
        click.echo("1. Create User")
        click.echo("2. Login")
        click.echo("3. Display All Users")  
        click.echo("4. Delete User by ID") 
        click.echo("5. Exit")

        choice_prompt =  "Enter your choice (1-5)"
        choice = click.prompt(choice_prompt, type=int)

        if current_user is not None and choice == 1:
            logout()
            break
        elif choice == 2:
            login()
        elif choice == 3:
            display_users()
        elif choice == 4:
            delete_user()  
        elif choice == 5:
            break
        elif current_user is None and choice == 1:
            create_user()
        else:
            click.echo("Invalid choice. Please enter a valid number.")
            
    if current_user is not None:
        save_session(current_user.username)

main_menu()

main_menu()

if __name__ == '__main__':
    cli()
    


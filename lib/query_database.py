from sqlalchemy.orm import sessionmaker
from models import User, Workout, Exercise, WorkoutExercises
from database import setup_database

# Call setup_database to get the engine
DBSession, engine = setup_database()

# Create a session
DBSession.configure(bind=engine)
session = DBSession()

# Query all users
users = session.query(User).all()

# Print user details
for user in users:
    print(f"User ID: {user.id}, Name: {user.name}, Age: {user.age}, Fitness Goals: {user.fitness_goals}")

# Query all workouts
workouts = session.query(Workout).all()

# Print workout details
for workout in workouts:
    print(f"Workout ID: {workout.id}, Date: {workout.date}, Duration: {workout.duration}, User ID: {workout.user_id}")

# Query all exercises
exercises = session.query(Exercise).all()

# Print exercise details
for exercise in exercises:
    print(f"Exercise ID: {exercise.id}, Name: {exercise.name}, Type: {exercise.type}, Difficulty: {exercise.difficulty}, Sets: {exercise.sets}, Reps: {exercise.reps}")

# Query all workout exercises
workout_exercises = session.query(WorkoutExercises).all()

# Print workout exercise details
for we in workout_exercises:
    print(f"Workout Exercise - Workout ID: {we.workout_id}, Exercise ID: {we.exercise_id}, Sets Completed: {we.sets_completed}, Reps Completed: {we.reps_completed}")

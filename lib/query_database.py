from sqlalchemy.orm import sessionmaker
from models import User, Workout, Exercise, WorkoutExercises
from database import setup_database

DBSession, engine = setup_database()

DBSession.configure(bind=engine)
session = DBSession()

users = session.query(User).all()

for user in users:
    print(f"User ID: {user.id}, Name: {user.name}, Age: {user.age}, Fitness Goals: {user.fitness_goals}")

workouts = session.query(Workout).all()

for workout in workouts:
    print(f"Workout ID: {workout.id}, Date: {workout.date}, Duration: {workout.duration}, User ID: {workout.user_id}")

exercises = session.query(Exercise).all()

for exercise in exercises:
    print(f"Exercise ID: {exercise.id}, Name: {exercise.name}, Type: {exercise.type}, Difficulty: {exercise.difficulty}, Sets: {exercise.sets}, Reps: {exercise.reps}")

workout_exercises = session.query(WorkoutExercises).all()

for we in workout_exercises:
    print(f"Workout Exercise - Workout ID: {we.workout_id}, Exercise ID: {we.exercise_id}, Sets Completed: {we.sets_completed}, Reps Completed: {we.reps_completed}")

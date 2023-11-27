from models.exercises import Exercise
from models.workouts import create_workout as create_new_workout


def helper_1():
    print("Performing useful function #1.")

def exit_program():
    print("Goodbye!")
    exit()

def create_workout():
    date = input("Enter workout date (YYYY-MM-DD): ")
    duration = int(input("Enter workout duration (minutes): "))

    exercises = []
    while True:
        exercise_name = input("Enter exercise name (type 'done' to finish): ")
        if exercise_name.lower() == 'done':
            break
        exercise_type = input("Enter exercise type: ")
        difficulty = input("Enter exercise difficulty: ")
        sets = int(input("Enter number of sets: "))
        reps = int(input("Enter number of reps: "))
        
        exercise = Exercise(exercise_name, exercise_type, difficulty, sets, reps)
        exercises.append(exercise)

    create_new_workout(date, duration, exercises)
    print("Workout created successfully!")

def workout_log():
    print("This is a workout log.")

def show_all_workouts():
    workouts = get_all_workouts() 
    for workout in workouts:
        print(f"Date: {workout.date}, Duration: {workout.duration} minutes")
        for exercise in workout.exercises:
            print(f"Exercise: {exercise.name}, Type: {exercise.exercise_type}, Difficulty: {exercise.difficulty}, Sets: {exercise.sets}, Reps: {exercise.reps}")
    print("These are all the workouts")

def show_all_users():
    print("These are all the users")

def delete_workout():
    print("Workout deleted.")

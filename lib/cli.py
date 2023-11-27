# lib/cli.py

from helpers import (
    exit_program,
    helper_1,
    create_workout,
    workout_log,
    show_all_workouts,
    show_all_users,
    delete_workout
)


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            create_workout()
        elif choice == "2":
            workout_log()
        elif choice == "3":
            show_all_workouts()
        elif choice == "4":
            show_all_users()
        elif choice == "5":
            delete_workout()    
        else:
            print("Invalid choice")


def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Create New Workout") 
    print("2. Workout Log") 
    print("3. Show All Workouts")
        #users using this workout
    print("4. Users")
        #print("4a. User All Workouts")
    print("5. Delete Workout")


if __name__ == "__main__":
    main()

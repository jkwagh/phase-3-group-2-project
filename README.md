## Table of Contents
- Installation
- Usage
- Main Menu
- User Menu
- Commands

## Installation
To use the Fitness Tracker CLI app, follow these steps:

- Clone the repository:
Copy code
git clone <repository_url>
- Install the required dependencies:
pip install -r requirements.txt
- Run the cli.py file:
python cli.py

## Usage

## Main Menu
Upon running the application, you'll be presented with the main menu. Here are the available options:

- Create User: Allows you to create a new user.

- Login: Log in as an existing user.

- Display All Users: Shows a table of all existing users.

- Delete User by ID: Deletes a user based on their ID.

- Exit: Exits the application.

## User Menu
- After logging in or creating a user, you'll enter the user menu. Here are the available options:

- Add Workout: Log a workout, including exercises.

- Delete Workout: Delete a workout by ID.

- Display User Workouts: Display all workouts for the logged-in user.

- Display Workouts: Display all workouts for all users.

- Add Exercise: Add a new exercise.

- Delete Exercise: Delete an exercise by ID.

- Display User Exercises: Display all exercises for the logged-in user.

- Display Exercises: Display all exercises for all users.

- Show Exercises in Workout: Display exercises associated with a specific workout.

- Logout: Log out the current user.

## Commands
- create_user: Create a new user with username, password, name, age, and fitness goals.
python cli.py create_user

- delete_user: Delete a user by ID.
python cli.py delete_user --user_id <user_id>

- add_workout: Add a workout, including exercises.
python cli.py add_workout

- delete_workout: Delete a workout by ID.
python cli.py delete_workout --workout_id <workout_id>

- display_users: Display a table of all users.
python cli.py display_users

- display_workouts: Display a table of all workouts.
python cli.py display_workouts

- display_exercises: Display a table of all exercises.
python cli.py display_exercises

- find_workout_exercises: Display exercises associated with a specific workout.
python cli.py find_workout_exercises --workout_id <workout_id>

- logout: Log out the current user.
python cli.py logout
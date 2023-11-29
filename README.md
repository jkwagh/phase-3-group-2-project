# Fitness Tracker CLI

## Overview
The Fitness Tracker CLI is a command-line interface for tracking users, workouts, and exercises. It provides functionality to create users, log workouts, add exercises, and more.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Creating a User](#creating-a-user)
  - [Deleting a User](#deleting-a-user)
  - [Adding a Workout](#adding-a-workout)
  - [Deleting a Workout](#deleting-a-workout)
  - [Displaying Users, Workouts, and Exercises](#displaying-users-workouts-and-exercises)
  - [Finding User, Workout, and Exercise by ID](#finding-user-workout-and-exercise-by-id)
  - [Adding and Deleting an Exercise](#adding-and-deleting-an-exercise)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/fitness-tracker-cli.git
   cd fitness-tracker-cli

## Install dependencies:
- pip install -r requirements.txt

## Setup the database:
- python database.py

## Usage
## Creating a User
- python cli.py create_user
- Follow the prompts to enter user information.

## Deleting a User
- python cli.py delete_user --user_id USER_ID
- Replace USER_ID with the ID of the user you want to delete.

## Adding a Workout
- python cli.py add_workout --user_id USER_ID --date YYYY-MM-DD --duration DURATION
- Replace USER_ID, YYYY-MM-DD, and DURATION with the appropriate values.

## Deleting a Workout
- python cli.py delete_workout --workout_id WORKOUT_ID
- Replace WORKOUT_ID with the ID of the workout you want to delete.

## Displaying Users, Workouts, and Exercises
- python cli.py display_users
- python cli.py display_workouts
- python cli.py display_exercises

## Finding User, Workout, and Exercise by ID
- python cli.py find_user --user_id USER_ID
- python cli.py find_workout --workout_id WORKOUT_ID
- python cli.py find_exercise --exercise_id EXERCISE_ID
- Replace USER_ID, WORKOUT_ID, and EXERCISE_ID with the desired IDs.

## Adding and Deleting an Exercise
- python cli.py add_exercise --name EXERCISE_NAME --type EXERCISE_TYPE --difficulty DIFFICULTY --sets SETS --reps REPS
- Replace EXERCISE_NAME, EXERCISE_TYPE, DIFFICULTY, SETS, and REPS with the appropriate values.
- python cli.py delete_exercise --exercise_id EXERCISE_ID
- Replace EXERCISE_ID with the ID of the exercise you want to delete.
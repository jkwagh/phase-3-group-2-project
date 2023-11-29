import sqlite3

CONN = sqlite3.connect('workouts.db')
CURSOR = CONN.cursor()

from sqlalchemy import Date, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as EnumType

Base = declarative_base()

class ExerciseType(EnumType):
    CORE = 'core'
    CARDIO = 'cardio'
    CHEST = 'chest'
    TRICEPS = 'triceps'
    SHOULDERS = 'shoulders'
    BACK = 'back'
    BICEPS = 'biceps'
    LEGS = 'legs'

class Exercise(Base):
    __tablename__ = 'exercises'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # Change EnumType to String
    difficulty = Column(Integer, nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('difficulty >= 1 AND difficulty <= 5', name='check_difficulty'),
        CheckConstraint("lower(type) IN ('core', 'cardio', 'chest', 'triceps', 'shoulders', 'back', 'biceps', 'legs')", name='check_exercise_type_lower')
    )

    workouts = relationship('WorkoutExercises', back_populates='exercise')

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    fitness_goals = Column(String)

    workouts = relationship('Workout', back_populates='user')

class Workout(Base):
    __tablename__ = 'workouts'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    duration = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='workouts')
    exercises = relationship('WorkoutExercises', back_populates='workout')

class WorkoutExercises(Base):
    __tablename__ = 'workout_exercises'

    workout_id = Column(Integer, ForeignKey('workouts.id'), primary_key=True)
    exercise_id = Column(Integer, ForeignKey('exercises.id'), primary_key=True)
    sets_completed = Column(Integer)
    reps_completed = Column(Integer)

    exercise = relationship('Exercise', back_populates='workouts')
    workout = relationship('Workout', back_populates='exercises')

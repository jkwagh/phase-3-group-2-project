from sqlalchemy import create_engine, Date, ForeignKey, Enum, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.types import Enum as EnumType
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm.exc import NoResultFound

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
    type = Column(String, nullable=False)
    difficulty = Column(Integer, nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('difficulty >= 1 AND difficulty <= 5', name='check_difficulty'),
        CheckConstraint("lower(type) IN ('core', 'cardio', 'chest', 'triceps', 'shoulders', 'back', 'biceps', 'legs')", name='check_exercise_type_lower')
    )

    workouts = relationship('WorkoutExercises', back_populates='exercise')

    @classmethod
    def create(cls, session, name, exercise_type, difficulty, sets, reps):
        exercise = cls(name=name, type=exercise_type, difficulty=difficulty, sets=sets, reps=reps)
        session.add(exercise)
        session.commit()
        return exercise

    @classmethod
    def delete(cls, session, exercise_id):
        exercise = cls.find_by_id(session, exercise_id)
        if exercise:
            session.delete(exercise)
            session.commit()

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, exercise_id):
        return session.query(cls).filter_by(id=exercise_id).first()

    @classmethod
    def get_user_exercises(cls, session, user_id):
        """Get exercises for a specific user."""
        return session.query(cls).join(WorkoutExercises).join(Workout).filter(Workout.user_id == user_id).all()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer)
    fitness_goals = Column(String)

    workouts = relationship('Workout', back_populates='user')

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def create(cls, session, username, password, name, age, fitness_goals):
        hashed_password = cls.set_password(password)
        user = cls(username=username, password_hash=hashed_password, name=name, age=age, fitness_goals=fitness_goals)
        session.add(user)
        session.commit()
        return user

    @classmethod
    def delete(cls, session, user_id):
        user = cls.find_by_id(session, user_id)
        if user:
            session.delete(user)
            session.commit()

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, user_id):
        return session.query(cls).filter_by(id=user_id).first()
    
    @classmethod
    def get_by_username(cls, session, username):
        try:
            return session.query(cls).filter(cls.username == username).one()
        except NoResultFound:
            return None
class Workout(Base):
    __tablename__ = 'workouts'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    duration = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='workouts')
    exercises = relationship('WorkoutExercises', back_populates='workout')

    @classmethod
    def create(cls, session, date, duration, user_id):
        workout = cls(date=date, duration=duration, user_id=user_id)
        session.add(workout)
        session.commit()
        return workout

    @classmethod
    def delete(cls, session, workout_id):
        workout = cls.find_by_id(session, workout_id)
        if workout:
            session.delete(workout)
            session.commit()

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, workout_id):
        return session.query(cls).filter_by(id=workout_id).first()

    @classmethod
    def get_user_workouts(cls, session, user_id):
        """Get workouts for a specific user."""
        return session.query(cls).filter(cls.user_id == user_id).all()

class WorkoutExercises(Base):
    __tablename__ = 'workout_exercises'

    workout_id = Column(Integer, ForeignKey('workouts.id'), primary_key=True)
    exercise_id = Column(Integer, ForeignKey('exercises.id'), primary_key=True)
    sets_completed = Column(Integer)
    reps_completed = Column(Integer)

    exercise = relationship('Exercise', back_populates='workouts')
    workout = relationship('Workout', back_populates='exercises')

    @classmethod
    def create(cls, session, workout_id, exercise_id, sets_completed, reps_completed):
        workout_exercise = cls(workout_id=workout_id, exercise_id=exercise_id, sets_completed=sets_completed, reps_completed=reps_completed)
        session.add(workout_exercise)
        session.commit()
        return workout_exercise

    @classmethod
    def delete(cls, session, workout_id, exercise_id):
        workout_exercise = cls.find_by_ids(session, workout_id, exercise_id)
        if workout_exercise:
            session.delete(workout_exercise)
            session.commit()

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_ids(cls, session, workout_id, exercise_id):
        return session.query(cls).filter_by(workout_id=workout_id, exercise_id=exercise_id).first()

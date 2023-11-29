from models.__init__ import CURSOR, CONN
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from faker import Faker

class Users:
    __tablename__ = "Users"
    def __init__(self, name, age, fitness_goals):
        self.name = name
        self.age = age
        self.fitness_goals = fitness_goals
        
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            print("Name must be a non-empty string")
            
    @property
    def age(self):
        return self._age
    @age.setter
    def age(self, age):
        if isinstance(age, int) and 1 < age < 99:
            self._age = age
        else:
            print("Age must be a number between 1 and 99")
            
    @property
    def fitness_goals(self):
        return self._fitness_goals
    @fitness_goals.setter
    def fitness_goals(self, fitness_goals):
        if isinstance(fitness_goals, str) and len(fitness_goals) < 140:
            self._fitness_goals = fitness_goals
        else:
            print("Fitness goals must be a string less than 140 characters")
            
    @classmethod
    def get_all(cls):
        """Return a list containing a Department object per row in the table"""
        sql = """
            SELECT *
            FROM departments
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    
# user1 = Users("Steve", 25, "To gain muscle")
# print(user1.name)
# print(user1.age)
# print(user1.fitness_goals)
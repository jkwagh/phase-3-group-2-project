class Exercise:
     
    def __init__(self, name, exercise_type, difficulty, sets, reps):
        self.name = name
        self.exercise_type = exercise_type
        self.difficulty = difficulty
        self.sets = sets
        self.reps = reps
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value):
            self._name = value
        else:
            print("Name must be a non-empty string")
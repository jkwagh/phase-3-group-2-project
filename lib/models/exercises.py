class Exercise:
    def __init__(self, name, exercise_type, difficulty, sets, reps):
        self._name = name
        self._exercise_type = exercise_type
        self._difficulty = difficulty
        self._sets = sets
        self._reps = reps

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value):
            self._name = value
        else:
            print("Name must be a non-empty string")

    @property
    def exercise_type(self):
        return self._exercise_type

    @exercise_type.setter
    def exercise_type(self, value):
        self._exercise_type = value

    @property
    def difficulty(self):
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value):
        self._difficulty = value

    @property
    def sets(self):
        return self._sets

    @sets.setter
    def sets(self, value):
        self._sets = value

    @property
    def reps(self):
        return self._reps

    @reps.setter
    def reps(self, value):
        self._reps = value


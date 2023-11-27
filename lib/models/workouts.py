class Workout:
    def __init__(self, date, duration, exercises):
        self.date = date
        self.duration = duration
        self.exercises = exercises

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value
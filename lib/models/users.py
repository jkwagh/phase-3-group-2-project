class Users:
    def __init__(self, name):
        self.name = name
        
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            print("name must be a non-empty string")

user1 = Users("Steve")
print(user1.name)
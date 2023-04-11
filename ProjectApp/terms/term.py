class term:
    def __init__(self, id, name):
        if not isinstance(id, int):
            raise TypeError("expecting an id of type int")
        if not isinstance(name, str):
            raise TypeError("expecting a name of type str")
        if id <= 0:
            raise ValueError("id must be positive")
        if len(name) > 6:
            raise ValueError("name must not exceed 6 characters")
        if not name:
            raise ValueError("name can not be null")
        self.id = id
        self.name = name
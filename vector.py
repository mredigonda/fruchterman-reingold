import math

class Vector:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x * other.x, self.y * other.y)
        else:
            return Vector(self.x * other, self.y * other)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    
    def toIntegerPair(self):
        return (math.floor(self.x), math.floor(self.y))
    
    def longitud(self):
        return math.sqrt(self.x**2 + self.y**2)

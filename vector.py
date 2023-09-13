PRINT_PRECISION = 4

class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def magnitude(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** .5

    def normalize(self):
        m = self.magnitude()
        self.x /= m
        self.y /= m
        self.z /= m
        return self

    def dot(self, other):
        if type(other) != Vector3:
            raise TypeError

        return self.x * other.x + self.y * other.y + self.z * other.z

    # Return COS between this and other vector
    def cos(self, other):
        if type(other) != Vector3:
            raise TypeError

        return self.dot(other) / (self.magnitude() * other.magnitude())

    def to_img(self, w, h):
        return (int(self.x * w), int(self.y * h))

    def ToJson(self):
        return [self.x, self.y, self.z]

    def copy(self, other):
        self.x = other.x
        self.y = other.y
        self.z = other.z

    def __add__(self, other):
        if type(other) != Vector3:
            raise TypeError

        return Vector3(self.x + other.x,
                       self.y + other.y,
                       self.z + other.z)

    def __sub__(self, other):
        if type(other) != Vector3:
            raise TypeError

        return Vector3(self.x - other.x,
                       self.y - other.y,
                       self.z - other.z)

    def __mul__(self, other):
        if type(other) == Vector3:
            raise TypeError

        return Vector3(self.x * other,
                       self.y * other,
                       self.z * other)

    def __truediv__(self, other):
        if type(other) == Vector3:
            raise TypeError

        return Vector3(self.x / other,
                       self.y / other,
                       self.z / other)

    def __str__(self):
        return f'({round(self.x, PRINT_PRECISION)}, {round(self.y, PRINT_PRECISION)}, {round(self.z, PRINT_PRECISION)})'

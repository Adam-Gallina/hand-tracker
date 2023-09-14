from math import cos, sin, degrees

PRINT_PRECISION = 4

def V3toDegree(v):
    return Vector3(degrees(v.x), degrees(v.y), degrees(v.z))

class Vector3:
    def __init__(self, x=0., y=0., z=0.):
        self.x = x
        self.y = y
        self.z = z

    # Could have issues with gimbal lock
    # Angle is in radians
    def rotate(self, angle):
        # Apply Z rotation
        x2 = cos(angle.z) * self.x - sin(angle.z) * self.y
        y2 = sin(angle.z) * self.x + cos(angle.z) * self.y
        # Apply Y rotation
        x3 = cos(angle.y) * x2 - sin(angle.y) * self.z
        z3 = sin(angle.y) * x2 + cos(angle.y) * self.z
        # Apply X rotation
        y4 = cos(angle.x) * y2 - sin(angle.x) * z3
        z4 = sin(angle.x) * y2 + cos(angle.x) * z3

        return Vector3(x3, y4, z4)

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

    def to_img(self, w, h, scale=1):
        return (int(self.x * w * scale), int(self.y * h * scale))

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

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __str__(self):
        return f'({round(self.x, PRINT_PRECISION)}, {round(self.y, PRINT_PRECISION)}, {round(self.z, PRINT_PRECISION)})'

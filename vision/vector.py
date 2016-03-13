''' 2D Vector classic implementing the basic vector functionality '''

import math


class Vector():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def toPoint(self):
        return (self.x, self.y)

    def magnitude(self):
        return (x ** 2 + y ** 2) ** (0.5)

    def rotate(self, angle):
        self.x = self.x * math.cos(angle) - self.x * math.sin(angle)
        self.y = self.y * math.sin(angle) + self.y * math.cos(angle)

    def rescale(self, desired_magnitude):
        self.x = self.x * desired_magnitude / self.magnitude()
        self.y = self.y * desired_magnitude / self.magnitude()

    @staticmethod
    def dotProduct(v1, v2):
        return v1.x * v2.x + v1.y * v2.y

    @staticmethod
    def angleBetween(v1, v2):

        dot_prod = dotProduct(v1, v2)
        cos_alpha = dot_prod / (v1.magnitude() * v2.magnitude())
        alpha = math.acos(cos_alpha)

        return math.degrees(alpha)

    @staticmethod
    def getDirectionVector( (cx, cy), (ox, oy), desired_magnitude ):

        diff_x = cx - ox
        diff_y = cy - oy

        if diff_x == 0:
            return (0, -diff_x)

        k = (cy - oy) / (cx - ox)
        if ox >= cx :
            dir_vector = Vector(1,k)
        else :
            dir_vector = Vector(-1, -k)

        dir_vector.rescale(desired_magnitude)

        return dir_vector

    @staticmethod
    def scalarMultiple(v, c):
        return Vector(v.x * c, v.y * c)
    @staticmethod
    def addToPoint((px, py), v):
        return (px + v.x, py + v.y)


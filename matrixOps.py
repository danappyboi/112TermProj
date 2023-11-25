import math

class matrix:
    def __init__(self, array):
        self.array = array
    
def rotateAlgo(velo, angle):
    #TODO: is angle in degrees or radians?
    return (math.cos(angle) * velo[0] + math.sin(angle) * velo[1]),(-math.sin(angle) * velo[0] + math.cos(angle) * velo[1])

def revertAlgo(velo, angle):
    return (math.cos(angle) * velo[0] - math.sin(angle) * velo[1]),(math.sin(angle) * velo[0] + math.cos(angle) * velo[1])

def dot(v1, v2):
    return (v1[0] * v2[0] + v1[1] * v2[1])

def dotScalar(c, v):
    return (c * v[0], c*v[1])

def add(v1, v2):
    return (v1[0] + v2[1], v1[1] + v2[1])
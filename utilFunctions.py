import math

#takes in cartesian coords and converts to python
def cartToPyX(x, width=600):
    """Converts from Cartseian coords to Python coords for x."""
    return x + width/2

def cartToPyY(y, height=600):
    """Converts from Cartiseasn coords to Python coords for y."""
    return -y + height/2

def pyToCartX(x, width=600):
    """Converts from Python coords to Cartisean"""
    return x - width/2

def pyToCartY(y, height=600):
    """Converts from Cartisean coords to Python coords"""
    return -(y - height/2)

def rotateAlgo(velo, angle):
    return (math.cos(angle) * velo[0] + math.sin(angle) * velo[1]),(-math.sin(angle) * velo[0] + math.cos(angle) * velo[1])

def revertAlgo(velo, angle):
    return (math.cos(angle) * velo[0] - math.sin(angle) * velo[1]),(math.sin(angle) * velo[0] + math.cos(angle) * velo[1])

def dot(v1, v2):
    """Finds the dot product of two tuples."""
    return (v1[0] * v2[0] + v1[1] * v2[1])

def dotScalar(c, v):
    """Finds the dot product of a scalar and tuples."""
    return (c * v[0], c*v[1])

def add(v1, v2):
    """Adds two tuples."""
    return (v1[0] + v2[1], v1[1] + v2[1])

import math
import os, pathlib
from cmu_graphics import*

def distance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5

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
    """A matrix I learned in 21-241 that finds the x,y of a point that has been rotated."""
    return (math.cos(angle) * velo[0] - math.sin(angle) * velo[1]),(math.sin(angle) * velo[0] + math.cos(angle) * velo[1])

def dot(v1, v2):
    """Finds the dot product of two tuples."""
    return (v1[0] * v2[0] + v1[1] * v2[1])

def dotScalar(c, v):
    """Finds the dot product of a scalar and tuples."""
    return (c * v[0], c*v[1])

def add(v1, v2):
    """Adds two tuples."""
    return (v1[0] + v2[0], v1[1] + v2[1])

def sign(n):
    """Dumb helper function to help determine the sign of a number."""
    if n == 0:
        return 0
    else:
        return int(n/abs(n))

#Gotz it from piazza
def loadSound(relativePath):
    # Convert to absolute path (because pathlib.Path only takes absolute paths)
    absolutePath = os.path.abspath(relativePath)
    # Get local file URL
    url = pathlib.Path(absolutePath).as_uri()
    # Load Sound file from local URL
    return Sound(url)

import math

#takes in cartesian coords and converts to python
def cartToPyX(x, width=600):
    """Converts from Cartseian coords to Python coords for x."""
    return x + width/2

def cartToPyY(y, height=600):
    """Converts from Cartiseasn coords to Python coords for y."""
    return -y + height/2

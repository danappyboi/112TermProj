import math
from cmu_graphics import*

#TODO: in theory, this means we can have multiple players, which is an interesting thought.
class player:
    """Not sure about the necessity of this class yet. For now, it holds each player's pocketed balls
        and whether or not the player uses striped balls."""
    
    def __init__(self, name):
        #TODO: boy wouldn't that be fancy?
        self.name = name
        self.pocketed = []
        self.striped = None
        self.turn = False
        self.AI = False
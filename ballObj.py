from cmu_graphics import*
from utilFunctions import*
import math

#TODO: there's no way I can't import these values straight from the main file
width = 600
height = 600
tableWidth = 225
tableHeight = 450

class ball:
    """The ball object. Has a x, y, color, and velocity. Used for all the balls and the cueball."""
    def __init__(self, posX, posY, color, striped=False, velo=(0,0), r=8, cueBall=False):
        self.posX = posX
        self.posY = posY
        self.color = color
        self.velo = velo
        self.r = r
        self.friction = .98
        self.pocketed = False
        self.striped = striped
        self.cueBall = cueBall

    def setVelo(self, velo):
        """Sets the velocity of the ball using a tuple."""
        self.velo = velo
    
    def getVeloVector(self):
        """Returns the magnitude of the velocity of the ball."""
        return math.sqrt(self.velo[0]**2 + self.velo[1]**2)
    
    def getVeloAngle(self):
        """Returns the angle of the velocity in degrees."""
        angle = abs(math.degrees(math.atan2(self.velo[1],self.velo[0])))
        if self.velo[0] >= 0 and self.velo[1] >= 0:
            return angle
        elif self.velo[0] >= 0 and self.velo[1] < 0:
            return -angle
        elif self.velo[0] < 0 and self.velo[1] >= 0:
            return 90 + angle
        else:
            return -(90 + angle)

    
    def setVeloVector(self, vector, angle):
        """Sets the velocity of the ball based on the magnitude and angle of the vector."""
        x = vector * math.cos(math.radians(angle))
        y = vector * math.sin(math.radians(angle))
        self.setVelo((x, y))

    def runVelo(self): 
        """How the velocity actually gets applied to the ball. Includes friction and wall collision."""
        newVeloX = self.velo[0] * self.friction
        newVeloY = self.velo[1] * self.friction
        if abs(self.velo[0]) <= 0.03:
            newVeloX = 0
        if abs(self.velo[1]) <= 0.03:
            newVeloY = 0
        self.setVelo((newVeloX, newVeloY))
        self.posX += self.velo[0]
        self.posY += self.velo[1]
        
        wallFriction = .1
        if self.wallCollisionX():
            self.setVelo((-self.velo[0] + sign(self.velo[0])*wallFriction, self.velo[1] + sign(self.velo[1])*wallFriction))
        if self.wallCollisionY():
            self.setVelo((self.velo[0] + sign(self.velo[0])*wallFriction, -self.velo[1] + sign(self.velo[1])*wallFriction))

    #TODO: pretty ball with animations?
    def draw(self):
        self.runVelo()
        x = cartToPyX(self.posX)
        y = cartToPyY(self.posY)
        drawCircle(x+1, y+1, self.r +1, fill=rgb(30, 30, 30), opacity=30)
        drawCircle(x, y, self.r, fill=self.color)
        drawCircle(x - 3, y - 3, 2, fill="white", opacity=70)

        # arrowMag = 8
        # drawLine(x, y, x + self.velo[0]* arrowMag, y - self.velo[1]* arrowMag, lineWidth = 3, arrowEnd=True, fill=self.color)

    def drawStatic(self, x, y):
        """Draws a static version of the ball. Could be changed later."""
        drawCircle(x+1, y+1, self.r +1, fill=rgb(30, 30, 30), opacity=30)
        drawCircle(x, y, self.r, fill=self.color)
        drawCircle(x - 3, y - 3, 2, fill="white", opacity=70)

    def wallCollisionX(self):
        """Determining whether or not the ball has collided with the left and right walls."""
        if not (-tableWidth/2 <= self.posX - self.r):
            self.posX = -tableWidth/2 + self.r
            return True
        elif not (self.posX + self.r <= tableWidth/2):
            self.posX = tableWidth/2 - self.r
            return True
        return False

    def wallCollisionY(self):
        """Determining whether or not the ball has collided with the top and bottom walls."""
        if not (tableHeight/2 >= self.posY + self.r):
            self.posY = tableHeight/2 - self.r
            return True
        elif not (self.posY - self.r >= -tableHeight/2):
            self.posY = -tableHeight/2 + self.r
            return True
        return False
    
def sign(n):
    """Dumb helper function to help determine the sign of a number."""
    if n == 0:
        return 0
    else:
        return n/abs(n)
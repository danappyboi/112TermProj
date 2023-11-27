import math
from cmu_graphics import*
from utilFunctions import*

class cueStickObj:
    """The object for the cueStick. Has a posX, posY, and angle. Also able to adjust the distance from the ball for visualizing power."""
    def __init__(self, posX, posY, angle):
        self.posX = cartToPyX(posX)
        self.posY = cartToPyY(posY)
        self.angle = -angle+90
        self.distFromBall = 20
    
    def addPower(self, newDist):
        """Adds power to the stick, and through gameElements, the power bar."""
        max = 100
        min = 1
        tot = self.distFromBall + newDist
        if min <= tot <= max:
            self.distFromBall += newDist
        elif tot > max:
            self.distFromBall = max
        elif tot < min:
            self.distFromBall = min

    def setAngle(self, angle):
        """Set the angle of the stick. Gotta plug it into a weird formula, so can't be changed directly."""
        self.angle = -angle -90

    #TODO: add some comments that really explain the math, its kinda hard to follow
    def draw(self, stickSize=300, aim=True):
        mathAngle = self.angle + 270 #the angle of the mouse and the angle used for math are different for some reason
        newPosY = self.posY
        #the y position of the stick changes depending on whether its above or below the ball. Weird.
        if not(self.angle % 360 < 90 or self.angle % 360 > 270):
            newPosY -= (stickSize + self.distFromBall + 9) * math.sin(math.radians(mathAngle))
        else:
            newPosY -= (self.distFromBall + 9) * math.sin(math.radians(mathAngle))

        drawRect(self.posX - ((stickSize)/2 + self.distFromBall + 9)* math.cos(math.radians(mathAngle)), newPosY,
            8, stickSize, fill=gradient("tan", "brown", start="top"), align="top", 
            rotateAngle = self.angle)
        
        self.aim(50)
    
    #TODO: it'd be pretty cool if it worked on walls and balls
    def aim(self, length):
        """Draws the dashed line used for aiming. Just a helper function to be used within the class."""
        endX = self.posX + length * -math.cos(math.radians(-(self.angle+90)))
        endY = self.posY + length * math.sin(math.radians(-(self.angle+90)))
        drawLine(self.posX, self.posY, endX, endY, fill="white", dashes=True)

    def hitCueBall(self, cueBall):
        """Sets the velo of the cueBall depending on the angle of the cueStick."""
        cueBall.setVeloVector(self.distFromBall * .5, (-(self.angle+90) + 180) % 360)
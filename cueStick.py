import math
from cmu_graphics import*
from pointConvert import*

class cueStickObj:
    """The object for the cueStick. Has a posX, posY, and angle. Also able to adjust the distance from the ball for visualizing power."""
    def __init__(self, posX, posY, angle):
        self.posX = cartToPyX(posX)
        self.posY = cartToPyY(posY)
        self.angle = -angle+90
        self.distFromBall = 20
    
    def setDistFromBall(self, newDist):
        self.distFromBall = newDist

    def setAngle(self, angle):
        self.angle = -angle -90

    #TODO: add some comments that really explain the math, its kinda hard to follow
    def draw(self, stickSize=300):
        mathAngle = self.angle + 270 #the angle of the mouse and the angle used for math are different for some reason
        newPosY = self.posY
        #the y position of the stick changes depending on whether its above or below the ball. Weird.
        if not(self.angle % 360 < 90 or self.angle % 360 > 270):
            newPosY -= (stickSize + self.distFromBall) * math.sin(math.radians(mathAngle))
        else:
            newPosY -= self.distFromBall * math.sin(math.radians(mathAngle))

        drawRect(self.posX - ((stickSize)/2 + self.distFromBall)* math.cos(math.radians(mathAngle)), newPosY,
            8, stickSize, fill=gradient("tan", "brown", start="top"), align="top", 
            rotateAngle = self.angle)

    def hitCueBall(self, cueBall, playing):
        cueBall.setVeloVector(self.distFromBall, (-(self.angle+90) + 180) % 360)
        print(f"cue angle:{(math.degrees(self.angle)) % 360}")
        playing = False
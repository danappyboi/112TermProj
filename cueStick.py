import math
from cmu_graphics import*
from pointConvert import*

class cueStickObj:
    def __init__(self, posX, posY, angle):
        self.posX = cartToPyX(posX)
        self.posY = cartToPyY(posY)
        self.angle = angle
        self.distFromBall = 20
    
    def setDistFromBall(self, newDist):
        self.distFromBall = newDist

    #TODO: because im chaning position, this is also probably fucked up, gotta fixxx
    def draw(self):
        mathAngle = self.angle + 270
        stickSize = 300
        newPosY = self.posY
        if not(self.angle % 360 < 90 or self.angle % 360 > 270):
            newPosY -= (stickSize + self.distFromBall) * math.sin(math.radians(mathAngle))
        else:
            newPosY -= self.distFromBall * math.sin(math.radians(mathAngle))

        drawRect(self.posX - ((stickSize)/2 + self.distFromBall)* math.cos(math.radians(mathAngle)), newPosY,
            8, stickSize, fill=gradient("tan", "brown", start="top"), align="top", 
            rotateAngle = self.angle)

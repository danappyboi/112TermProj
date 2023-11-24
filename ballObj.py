from cmu_graphics import*
import pointConvert
import math

width = 600
height = 600
tableWidth = 250
tableHeight = 500

class ball:
    def __init__(self, posX, posY, color, velo=(0,0), r=8):
        self.posX = posX
        self.posY = posY
        self.color = color
        self.velo = velo
        self.r = r
        self.friction = .07

    def setVelo(self, velo):
        self.velo = velo
    
    def getVeloVector(self):
        return math.sqrt(self.velo[0]**2 + self.velo[1]**2)
    
    def getVeloAngle(self):
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
        x = vector * math.cos(math.radians(angle))
        y = vector * math.sin(math.radians(angle))
        self.setVelo((x, -y))

    def runVelo(self): 
        frictionX = -sign(self.velo[0]) * self.friction
        frictionY = -sign(self.velo[1]) * self.friction

        newVeloX = self.velo[0] + frictionX
        newVeloY = self.velo[1] + frictionY
        if abs(self.velo[0] + frictionX) <= 0.05:
            newVeloX = 0
        if abs(self.velo[1] + frictionY) <= 0.05:
            newVeloY = 0
        self.setVelo((newVeloX, newVeloY))
        self.posX += self.velo[0]
        self.posY += self.velo[1]
        
        wallFriction = .1
        if self.wallCollisionX():
            self.setVelo((-self.velo[0] + sign(self.velo[0])*wallFriction, self.velo[1] + sign(self.velo[1])*wallFriction))
        if self.wallCollisionY():
            self.setVelo((self.velo[0] + sign(self.velo[0])*wallFriction, -self.velo[1] + sign(self.velo[1])*wallFriction))

    def draw(self):
        self.runVelo()
        x = pointConvert.cartToPyX(self.posX)
        y = pointConvert.cartToPyY(self.posY)
        drawCircle(self.posX, self.posY, self.r, fill=self.color)
        arrowMag = 8
        drawLine(self.posX, self.posY, self.posX + self.velo[0]* arrowMag, self.posY + self.velo[1]* arrowMag, lineWidth = 3, arrowEnd=True, fill=self.color)


    def wallCollisionX(self):
        if not ((width-tableWidth)/2 <= self.posX - self.r):
            self.posX = (width-tableWidth)/2 + self.r
            return True
        elif not (self.posX + self.r<= (width-tableWidth)/2 + tableWidth):
            self.posX = (width-tableWidth)/2 + tableWidth - self.r
            return True
        return False

    def wallCollisionY(self):
        if not ((height-tableHeight)/2 <= self.posY - self.r):
            self.posY = (height-tableHeight)/2 + self.r
            return True
        elif not (self.posY + self.r <= (height-tableHeight)/2 + tableHeight):
            self.posY = (height-tableHeight)/2 + tableHeight - self.r
            return True
        return False
    
def sign(n):
    if n == 0:
        return 0
    else:
        return n/abs(n)
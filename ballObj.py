from cmu_graphics import*
import math

class ball:
    def __init__(self, posX, posY, color, velo=(0,0), r=8):
        self.posX = posX
        self.posY = posY
        self.color = color
        self.velo = velo
        self.r = r

    def setVelo(self, velo):
        self.velo = velo
    
    def getVeloVector(self):
        return math.sqrt(self.velo[0]**2 + self.velo[1]**2)
    
    def getVeloAngle(self):
        return math.degrees(math.atan2(self.velo[1],self.velo[0]))
    
    def setVeloVector(self, vector, angle):
        x = vector * math.cos(math.radians(angle))
        y = vector * math.sin(math.radians(angle))
        self.setVelo((x, y))

    def runVelo(self):  
        self.posX += self.velo[0]
        self.posY += self.velo[1]
        
        if self.wallCollisionX():
            self.setVelo((-self.velo[0], self.velo[1]))
        if self.wallCollisionY():
            self.setVelo((self.velo[0], -self.velo[1]))

    def draw(self):
        self.runVelo()
        drawCircle(self.posX, self.posY, self.r, fill=self.color)


    def wallCollisionX(self):
        if not (75 <= self.posX - self.r):
            self.posX = 75 + self.r
            return True
        elif not (self.posX + self.r<= 325):
            self.posX = 325 - self.r
            return True
        return False

    def wallCollisionY(self):
        if not (50 <= self.posY - self.r):
            self.posY = 50 + self.r
            return True
        elif not (self.posY + self.r <= 550):
            self.posY = 550 - self.r
            return True
        return False
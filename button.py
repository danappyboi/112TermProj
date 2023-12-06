from cmu_graphics import*
from utilFunctions import loadSound

clackSound = loadSound("clackSound.mp3")

class button: 
    def __init__(self, x, y, width, height, visible=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = visible
        self.highlight = False

    def setVisible(self, visible):
        self.visible = visible

    def drawButtonImage(self, image):
        if self.visible:
            drawImage(image, self.x, self.y, width=self.width, height=self.width, align="center")

    def drawButtonGraphic(self, text, color=rgb(50,50,50), opacity=90):
        if self.visible:
            if self.highlight:
                borderThickness = 5
            else:
                borderThickness = 2
            drawRect(self.x, self.y, self.width, self.height, align="center", border="white", borderWidth=borderThickness, fill=color,opacity=opacity)
            drawLabel(text, self.x, self.y, size=self.height*.3, fill="white", font="orbitron")

    def clicked(self, mouseX, mouseY):
        if self.visible:
            if (self.x - self.width/2 < mouseX < self.x + self.width/2):
                if (self.y - self.height/2 < mouseY < self.y + self.height/2):
                    clackSound.play(restart=True)
                    return True
        return False
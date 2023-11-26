from cmu_graphics import *
import math
from ballObj import ball
from matrixOps import*
from pointConvert import*
from cueStick import cueStickObj
import gameElements

def onAppStart(app):
    app.background = "green"
    app.width = 600
    app.height = 600
    app.tick = 0
    app.spinning = False
    app.striped = False

def redrawAll(app):
    x = app.width/2
    y = app.height/2
    r = 100
    color = "red"
    num = 1
    if not app.spinning:
        if not app.striped:
            drawCircle(x+r*.03, y+r*.03, r + r*.03, fill=rgb(30, 30, 30), opacity=30)
            drawCircle(x, y, r, fill=color)
            drawCircle(x, y, 40, fill="white")
            drawLabel(num, x-3, y, size=60, bold=True)
            drawCircle(x - r*.32, y - r*.32, r*.2, fill="white", opacity=70)
        else:
            drawCircle(x+r*.03, y+r*.03, r + r*.03, fill=rgb(30, 30, 30), opacity=30)
            drawCircle(x, y, r, fill="white")
            drawRect(x, y, 150, 125, fill=color, align="center")
            drawOval(x-75, y, 50, 125, fill=color, align="center")
            drawOval(x+75, y, 50, 125, fill=color, align="center")
            drawCircle(x, y, 40, fill="white")
            drawLabel(num, x-3, y, size=60, bold=True)
            drawCircle(x - r*.32, y - r*.32, r*.2, fill="white", opacity=70)
    else:
        """TODO: here's the plan for spinning balls: 
            create 8 different frames for each orentaion of the ball, and based on
            the tick (don't ask me how to access tick from each ball), switch between 
            each frame. This can be done by creating ovals at each corner of the ball,
            and using the velocity to detemine which set of pictures to use.

            Note: might be easier to just make them in google drawings and then put them here, 
            ovals are a pain in the dick.
        """
        if not app.striped:
            drawCircle(x+r*.03, y+r*.03, r + r*.03, fill=rgb(30, 30, 30), opacity=30)
            drawCircle(x, y, r, fill=color)
            drawCircle(x, y, 40, fill="white")
            drawCircle(x - r*.32, y - r*.32, r*.2, fill="white", opacity=70)



def onKeyHold(app, keys):
    if "space" in keys:
        app.spinning = True
    if "s" in keys:
        app.striped = True

def onKeyRelease(app, key):
    if key == "space":
        app.spinning = False
    if key == "s":
        app.striped = False

def onStep(app):
    app.tick += 1
def main():
    runApp()

main()


from cmu_graphics import *
import math
from ballObj import ball
from matrixOps import*
from pointConvert import*
from cueStick import cueStickObj
import gameElements

def onAppStart(app):
    app.background = "black"
    app.width = 600
    app.height = 600
    app.tableWidth = 225
    app.tableHeight = 450
    app.pockets = [app.width/2 - app.tableWidth/2, app.height/2 - app.tableHeight/2,
                   app.width/2 + app.tableWidth/2, app.height/2 - app.tableHeight/2,
                   app.width/2 + app.tableWidth/2, app.height/2,
                   app.width/2 + app.tableWidth/2, app.height/2 + app.tableHeight/2,
                   app.width/2 - app.tableWidth/2, app.height/2 + app.tableHeight/2,
                   app.width/2- app.tableWidth/2, app.height/2]
    app.angle = 180

    app.redBall = ball(0, 0 + 200, "red", velo=(0,0))
    app.cueBall = ball(0,0 - 100, "lightGrey", velo=(0, 0))
    app.ballList = [app.cueBall, app.redBall]

    app.cueStick = cueStickObj(app.cueBall.posX, app.cueBall.posY, app.angle)

    app.playing = True


def redrawAll(app):
    drawRect(app.width/2, app.height/2, app.tableWidth + 25, app.tableHeight + 25, fill="brown", align="center")
    drawRect(app.width/2, app.height/2, app.tableWidth, app.tableHeight, fill="green", align="center")
    for i in range(int(len(app.pockets)/2)):
        drawCircle(app.pockets[i * 2], app.pockets[i * 2 + 1], 11, fill="black")

    # drawing the ball
    for ball in app.ballList:
        ball.draw()

    #drawing cueStick
    if app.playing == True:
        app.cueStick.posX = cartToPyX(app.cueBall.posX)
        app.cueStick.posY = cartToPyY(app.cueBall.posY)
        app.cueStick.draw()

    #drawing powerBar
    gameElements.drawPowerBar(app.width/2, app.height - 35, app.cueStick.distFromBall)
    
    
    # testingNotes(app, app.ballList)

def testingNotes(app, ballList):
    spacing = 100
    gap = 15
    for i in range(len(ballList)):
        ball = ballList[i]
        veloStat = (math.ceil(ball.velo[0]*1000)/1000, math.ceil(ball.velo[1]*1000)/1000) 
        xStat = math.ceil(ball.posX*1000)/1000
        yStat = math.ceil(ball.posY*1000)/1000
        drawLabel(f"{ball.color}", 50, i * spacing + 50, fill="white", size=10)
        drawLabel(veloStat, 50, i * spacing + 50 + gap, fill="white", size=10)
        drawLabel(f"Pos: {xStat}, {yStat}", 50, i * spacing + 50 + gap*2, fill="white", size=10)
        drawLabel(f"Pos: {pointConvert.cartToPyX(xStat)}, {pointConvert.cartToPyY(yStat)}", 50, i * spacing + 50 + gap*3, fill="white", size=10)



def onMouseMove(app, mouseX, mouseY):
    posX = app.cueBall.posX
    posY = app.cueBall.posY
    app.angle = -math.degrees(math.atan2(mouseY - cartToPyY(posY), mouseX - cartToPyX(posX)))
    app.cueStick.setAngle(app.angle)
    # print(f"main app.angle: {app.angle}")
#     pass

def onKeyPress(app, key):
    if app.playing == True:
        if key == "a" or key == "left":
            app.cueStick.addPower(-1) #TODO: might make more sense to call this power
        if key == "d" or key == "right":
            app.cueStick.addPower(1)
        if key == "space":
                app.cueStick.hitCueBall(app.cueBall, app.playing)
    

def onKeyHold(app, keys):
    if "left" in keys or "a" in keys:
        app.cueStick.addPower(-3)
    if "right" in keys or "d" in keys:
        app.cueStick.addPower(3)
#     pass

def onStep(app):
    gameElements.checkBallCollisions(app.ballList)
    

def main():
    runApp()

main()


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
    #TODO: the pockets work, but is it too easy?
    pocketShift = 5
    app.pockets = [[app.width/2 - app.tableWidth/2 + pocketShift, app.height/2 - app.tableHeight/2 + pocketShift],
                   [app.width/2 + app.tableWidth/2 - pocketShift, app.height/2 - app.tableHeight/2 + pocketShift],
                   [app.width/2 + app.tableWidth/2 - pocketShift, app.height/2],
                   [app.width/2 + app.tableWidth/2 - pocketShift, app.height/2 + app.tableHeight/2 - pocketShift],
                   [app.width/2 - app.tableWidth/2 + pocketShift, app.height/2 + app.tableHeight/2 - pocketShift],
                   [app.width/2- app.tableWidth/2 + pocketShift, app.height/2]]
    app.angle = 180

    app.redBall = ball(0, 200, "red", velo=(0,0))
    app.blueBall = ball(0 - 18,200, "blue", velo=(0,0))
    app.greenBall = ball(0 - 18 * 2, 200, "lime", velo=(0,0))
    app.orangeBall = ball(0 - 18 * 3, 200, "orange", velo=(0,0))
    app.yellowBall = ball(0 + 18,200, "yellow", velo=(0,0))
    app.blackBall = ball(0 + 18 * 2, 200, "black", velo=(0,0))
    app.purpleBall = ball(0 - 18 * 1.5, 200 - 18, "purple", velo=(0,0))
    app.pinkBall = ball(0 - 18 * 0.5, 200 - 18, "pink", velo=(0,0))
    app.grayBall = ball(0 + 18 * 1.5, 200 - 18, "gray", velo=(0,0))
    app.lightBall = ball(0 + 18 * .5, 200 - 18, "lightBlue", velo=(0,0))

    app.ball1 = ball(0 + 18, 200 - 18 * 2, 'mediumVioletRed', velo=(0,0))
    app.ball2 = ball(0 - 18, 200 - 18 * 2, 'brown', velo=(0,0))
    app.ball3 = ball(0, 200 - 18 * 2, 'darkSlateGray', velo=(0,0))
    app.ball4 = ball(0 - 18 * .5, 200 - 18 * 3, 'fireBrick', velo=(0,0))
    app.ball5 = ball(0 + 18 * .5, 200 - 18 * 3, 'gold', velo=(0,0))
    app.ball6 = ball(0, 200 - 18 * 4, 'darkTurquoise', velo=(0,0))

    app.cueBall = ball(0, 0 - 100, "lightGrey", velo=(0,0))

    app.ballList = [app.cueBall, app.redBall, app.blueBall, app.greenBall, 
                    app.yellowBall, app.blackBall, app.purpleBall, app.pinkBall, 
                    app.grayBall, app.lightBall, app.ball1, app.ball2,
                    app.ball3, app.ball4, app.ball5, app.ball6]
    
    app.player1Pocket = []
    app.player2Pocket = []

    app.cueStick = cueStickObj(app.cueBall.posX, app.cueBall.posY, app.angle)

    app.playing = True


def redrawAll(app):
    drawRect(app.width/2, app.height/2, app.tableWidth + 25, app.tableHeight + 25, fill="brown", align="center")
    drawRect(app.width/2, app.height/2, app.tableWidth, app.tableHeight, fill="green", align="center")
    for i in range(int(len(app.pockets))):
        drawCircle(app.pockets[i][0], app.pockets[i][1], 11, fill="black")

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

    #draw leftPocketed
    gameElements.drawLeftPockets(app.player1Pocket)
    
    
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
        if key == "s" or key == "down":
            app.cueStick.addPower(-1) #TODO: might make more sense to call this power
        if key == "w" or key == "up":
            app.cueStick.addPower(1)
        if key == "space":
                app.cueStick.hitCueBall(app.cueBall)
                app.playing = False
    

def onKeyHold(app, keys):
    if "left" in keys or "a" in keys:
        app.cueStick.addPower(-3)
    if "right" in keys or "d" in keys:
        app.cueStick.addPower(3)

def onStep(app):
    if not app.playing:
        gameElements.checkBallCollisions(app.ballList)
        gameElements.checkingPockets(app.ballList, app.pockets, app.player2Pocket, app.player1Pocket)
        if gameElements.ballsStopped(app.ballList):
            app.playing = True  

def main():
    runApp()

main()


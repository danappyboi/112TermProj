from cmu_graphics import *
import math
from ballObj import ball
from utilFunctions import*
from cueStick import cueStickObj
import gameElements
from player import player
import ai
import ballPositions


def onAppStart(app):
    app.background = rgb(20, 30, 20)
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

    # app.red1 = ball(0, 200, "red", striped = True, velo=(0,0))
    # app.red2 = ball(0 - 18,200, "red",striped = True, velo=(0,0))
    # app.red3 = ball(0 - 18 * 2, 200, "red",striped = True, velo=(0,0))
    # app.red4 = ball(0 - 18 * 3, 200, "red",striped = True, velo=(0,0))
    # app.red5 = ball(0 + 18,200, "red",striped = True, velo=(0,0))
    # app.blue1 = ball(0 + 18 * 2, 200, "blue", velo=(0,0))
    # app.blue2 = ball(0 - 18 * 1.5, 200 - 18, "blue", velo=(0,0))
    # app.blue3 = ball(0 - 18 * 0.5, 200 - 18, "blue", velo=(0,0))
    # app.blue4 = ball(0 + 18 * 1.5, 200 - 18, "blue", velo=(0,0))
    # app.blue5 = ball(0 + 18 * .5, 200 - 18, "blue", velo=(0,0))

    app.cueBall = ball(0, -100, "lightGrey", velo=(0,0), cueBall = True)
    app.redTest = ball(50, 60, "red", striped = True, velo=(0,0))
    app.blueTest = ball(45, -70, "blue", velo=(0,0))

    app.ballList = [app.cueBall, app.redTest, app.blueTest]
    # app.ballList = [app.cueBall, app.red1, app.red2, app.red3, 
    #                 app.red4, app.red5, app.blue1, app.blue2, 
    #                 app.blue3, app.blue4, app.blue5]
    

    # ballPositions.totalBallSetup()
    # ballPositions.testPhysics()

    app.player1 = player("Player 1")
    app.player1.turn = True
    app.player1.striped = True
    app.player2 = player("AI")
    app.AI = player("Actual AI")
    app.nonStripedBalls = []
    app.stripedBalls = []

    app.testBallList =[]
    app.testPoint = (0,0)
    app.testPoint1 = (0,0)

    app.cueStick = cueStickObj(app.cueBall.posX, app.cueBall.posY, app.angle)

    app.playing = True
    app.firstBallPocketed = False
    app.scratch = True


def redrawAll(app):
    drawRect(app.width/2, app.height/2, app.tableWidth + 25, app.tableHeight + 25, fill="brown", align="center")
    drawRect(app.width/2, app.height/2, app.tableWidth, app.tableHeight, fill="green", align="center")
    for i in range(int(len(app.pockets))):
        drawCircle(app.pockets[i][0], app.pockets[i][1], 11, fill="black")
        drawLabel(i,app.pockets[i][0], app.pockets[i][1], size=15,fill="white")

    # drawing the ball
    for ball in app.ballList:
        ball.draw()

    #drawing cueStick
    if app.playing and not app.scratch:
        app.cueStick.posX = cartToPyX(app.cueBall.posX)
        app.cueStick.posY = cartToPyY(app.cueBall.posY)
        app.cueStick.draw()

    #drawing powerBar
    gameElements.drawPowerBar(app.width/2, app.height - 35, app.cueStick.distFromBall)

    #draw leftPocketed
    gameElements.drawPlayerHuds(app.player1, app.player2)
    
    # print(app.testPoint[0], app.testPoint[1])
    drawCircle(cartToPyX(app.testPoint[0]), cartToPyY(app.testPoint[1]), 5, fill="white")
    drawCircle(cartToPyX(app.testPoint1[0]), cartToPyY(app.testPoint1[1]), 5, fill="red")
    # testing(app,app.redTest,app.pockets[1])


def testing(app, ball, pocket):
    """a function for anything being tested"""
    dxBTP = ball.posX - pyToCartX(pocket[0])
    dyBTP = ball.posY - pyToCartY(pocket[1])

    angleToPocket = math.degrees(math.atan2(dyBTP,dxBTP))

    hypoCueX = ball.posX + 2 * ball.r * math.cos(math.radians(angleToPocket))
    hypoCueY = ball.posY + 2 * ball.r * math.sin(math.radians(angleToPocket))

    drawCircle(cartToPyX(hypoCueX), cartToPyY(hypoCueY), 5, fill="purple")
    drawLine(cartToPyX(hypoCueX), cartToPyY(hypoCueY), pocket[0], pocket[1])

def onMouseMove(app, mouseX, mouseY):
    if app.AI.turn == False:
        if app.scratch:
            app.cueBall.setVelo((0,0))
            app.cueBall.pocketed = False
            if app.cueBall not in app.ballList:
                app.ballList.append(app.cueBall)
            app.cueBall.posX = pyToCartX(mouseX)
            app.cueBall.posY = pyToCartY(mouseY)
        else:
            posX = app.cueBall.posX
            posY = app.cueBall.posY
            app.angle = -math.degrees(math.atan2(mouseY - cartToPyY(posY), mouseX - cartToPyX(posX)))
            app.cueStick.setAngle(app.angle)

def onMousePress(app, mouseX, mouseY):
    if app.scratch:
        app.scratch = False

def onKeyPress(app, key):
    if app.playing == True:
        if key == "s" or key == "down":
            app.cueStick.addPower(-1) #TODO: might make more sense to call this power
        if key == "w" or key == "up":
            app.cueStick.addPower(1)
        if key == "space":
            app.cueStick.hitCueBall(app.cueBall)
            app.playing = False
        #For testing:
        if key == "enter":
            # aiAngle = ai.determineBestAngle(app.redTest, app.pockets[1], app.cueBall)
            # aiPower = ai.determineBestPower(app.cueBall, app.redTest, app.pockets[1])
            # print(aiAngle)
            # app.cueStick.setAngle(aiAngle)
            # app.cueStick.setPower(aiPower)
            # app.cueStick.hitCueBall(app.cueBall)
            app.testPoint = (app.cueBall.posX, app.cueBall.posY)
            app.testPoint1 = (app.redTest.posX, app.redTest.posY)
            ai.hitTheBall(app.cueStick, app.cueBall, app.ballList, app.pockets, True)
            app.playing = False
    

def onKeyHold(app, keys):
    if "left" in keys or "a" in keys:
        app.cueStick.addPower(-3)
    if "right" in keys or "d" in keys:
        app.cueStick.addPower(3)

def onStep(app):
    if not app.playing:
        gameElements.checkBallCollisions(app.ballList)
        gameElements.checkingPockets(app.ballList, app.pockets, app.stripedBalls, app.nonStripedBalls)
        if gameElements.ballsStopped(app.ballList):
            if app.player1.turn: 
                gameElements.turnLogic(app, app.player1, app.player2, app.stripedBalls, app.nonStripedBalls, app.cueBall)
            else:
                gameElements.turnLogic(app, app.player2, app.player1, app.stripedBalls, app.nonStripedBalls, app.cueBall)
            app.playing = True  

def main():
    runApp()

main()


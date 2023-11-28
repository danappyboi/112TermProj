from cmu_graphics import *
import math
from ballObj import ball
from utilFunctions import*
from cueStick import cueStickObj
import gameElements
from player import player
import ai


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

    app.red1 = ball(-50, + 50, "red", striped = True, velo=(0,0))
    app.red2 = ball(0 - 18,200, "red",striped = True, velo=(0,0))
    app.red3 = ball(0 - 18 * 2, 200, "red",striped = True, velo=(0,0))
    app.red4 = ball(0 - 18 * 3, 200, "red",striped = True, velo=(0,0))
    app.red5 = ball(0 + 18,200, "red",striped = True, velo=(0,0))
    app.blue1 = ball(0 + 18 * 2, 200, "blue", velo=(0,0))
    app.blue2 = ball(0 - 18 * 1.5, 200 - 18, "blue", velo=(0,0))
    app.blue3 = ball(0 - 18 * 0.5, 200 - 18, "blue", velo=(0,0))
    app.blue4 = ball(0 + 18 * 1.5, 200 - 18, "blue", velo=(0,0))
    app.blue5 = ball(0 + 18 * .5, 200 - 18, "blue", velo=(0,0))

    app.cueBall = ball(100, 100, "lightGrey", velo=(0,0), cueBall = True)

    app.ballList = [app.cueBall, app.red1]
    # app.ballList = [app.cueBall, app.red1, app.red2, app.red3, 
    #                 app.red4, app.red5, app.blue1, app.blue2, 
    #                 app.blue3, app.blue4, app.blue5]
    
    app.player1 = player("Player 1")
    app.player1.turn = True
    app.player1.striped = True
    app.player2 = player("AI")
    app.AI = player("Actual AI")
    app.nonStripedBalls = []
    app.stripedBalls = []

    app.testBallList =[]

    app.cueStick = cueStickObj(app.cueBall.posX, app.cueBall.posY, app.angle)

    app.playing = True
    app.firstBallPocketed = False
    app.scratch = False


def redrawAll(app):
    drawRect(app.width/2, app.height/2, app.tableWidth + 25, app.tableHeight + 25, fill="brown", align="center")
    drawRect(app.width/2, app.height/2, app.tableWidth, app.tableHeight, fill="green", align="center")
    for i in range(int(len(app.pockets))):
        drawCircle(app.pockets[i][0], app.pockets[i][1], 11, fill="black")

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
    
    
    # testing(app, app.ballList)


def testing(app, ballList):
    """a function for anything being tested"""
    for ball in ballList:
        if not ball.cueBall:
            dxBTB = app.cueBall.posX - ball.posX
            dyBTB = app.cueBall.posY - ball.posY

            pos1 = revertAlgo((0 + 2 * ball.r, 0), math.atan2(dyBTB, dxBTB) - math.pi/2)
            pos2 = revertAlgo((0 - 2 * ball.r, 0), math.atan2(dyBTB, dxBTB) - math.pi/2)
            pos1 = add(pos1, (ball.posX, ball.posY))
            pos2 = add(pos2, (ball.posX, ball.posY))

            drawCircle(cartToPyX(pos1[0]), cartToPyY(pos1[1]), 5, fill="purple", border="black")
            drawCircle(cartToPyX(pos2[0]), cartToPyY(pos2[1]), 5, fill="purple", border="black")


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
            aiAngle = ai.determineBestAngle(app.red1, app.pockets[5], app.cueBall)
            aiPower = ai.determineBestMagnitude(app.cueBall, app.red1, app.pockets[5])
            app.cueStick.setAngle(aiAngle)
            app.cueStick.setPower(aiPower)
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
        gameElements.checkingPockets(app.ballList, app.pockets, app.stripedBalls, app.nonStripedBalls)
        if gameElements.ballsStopped(app.ballList):
            if app.player1.turn: 
                gameElements.turnLogic(app, app.player1, app.player2, app.stripedBalls, app.nonStripedBalls, app.cueBall)
                print(app.cueBall.posY)
            else:
                gameElements.turnLogic(app, app.player2, app.player1, app.stripedBalls, app.nonStripedBalls, app.cueBall)
            app.playing = True  

def main():
    runApp()

main()


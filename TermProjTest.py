from cmu_graphics import *
import math
from ballObj import ball
from utilFunctions import*
from cueStick import cueStickObj
import gameElements
from player import player


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

    app.red1 = ball(0, 200, "red", striped = True, velo=(0,0))
    app.red2 = ball(0 - 18,200, "red",striped = True, velo=(0,0))
    app.red3 = ball(0 - 18 * 2, 200, "red",striped = True, velo=(0,0))
    app.red4 = ball(0 - 18 * 3, 200, "red",striped = True, velo=(0,0))
    app.red5 = ball(0 + 18,200, "red",striped = True, velo=(0,0))
    app.blue1 = ball(0 + 18 * 2, 200, "blue", velo=(0,0))
    app.blue2 = ball(0 - 18 * 1.5, 200 - 18, "blue", velo=(0,0))
    app.blue3 = ball(0 - 18 * 0.5, 200 - 18, "blue", velo=(0,0))
    app.blue4 = ball(0 + 18 * 1.5, 200 - 18, "blue", velo=(0,0))
    app.blue5 = ball(0 + 18 * .5, 200 - 18, "blue", velo=(0,0))

    app.cueBall = ball(0, 0 - 100, "lightGrey", velo=(0,0), cueBall = True)

    app.ballList = [app.cueBall, app.red1, app.red2, app.red3, 
                    app.red4, app.red5, app.blue1, app.blue2, 
                    app.blue3, app.blue4, app.blue5]
    
    app.player1 = player("Player 1")
    app.player1.turn = True
    app.player1.striped = True
    app.player2 = player("AI")
    app.nonStripedBalls = []
    app.stripedBalls = []

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
        drawLabel(f"Pos: {cartToPyX(xStat)}, {cartToPyY(yStat)}", 50, i * spacing + 50 + gap*3, fill="white", size=10)


def onMouseMove(app, mouseX, mouseY):
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
            # if app.cueBall.pocketed:
            #     app.ballList.append(app.cueBall)
            #     app.cueBall.pocketed = False
            if app.player1.turn: 
                gameElements.turnLogic(app, app.player1, app.player2, app.stripedBalls, app.nonStripedBalls, app.cueBall)
            else:
                gameElements.turnLogic(app, app.player2, app.player1, app.stripedBalls, app.nonStripedBalls, app.cueBall)
            app.playing = True  

def main():
    runApp()

main()


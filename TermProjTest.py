from cmu_graphics import *
import math
from ballObj import ball
from utilFunctions import*
from cueStick import cueStickObj
import gameElements
from player import player
import ai
import ballPositions
import copy
from button import button

#TODO: fix going too fast
#TODO: resize...?

def onAppStart(app):
    app.background = rgb(20, 30, 20)
    app.width = 600
    app.height = 600
    app.tableWidth = 225
    app.tableHeight = 450
    pocketShift = 7
    app.pockets = [[app.width/2 - app.tableWidth/2 + pocketShift, app.height/2 - app.tableHeight/2 + pocketShift],
                   [app.width/2 + app.tableWidth/2 - pocketShift, app.height/2 - app.tableHeight/2 + pocketShift],
                   [app.width/2 + app.tableWidth/2 - pocketShift, app.height/2],
                   [app.width/2 + app.tableWidth/2 - pocketShift, app.height/2 + app.tableHeight/2 - pocketShift],
                   [app.width/2 - app.tableWidth/2 + pocketShift, app.height/2 + app.tableHeight/2 - pocketShift],
                   [app.width/2- app.tableWidth/2 + pocketShift, app.height/2]]
    app.angle = 180

    ballPositions.officialBallSetup()
    app.ballList = copy.copy(app.initalBallList)

    app.player1 = player("Player 1")
    app.AIPlayer = player("AI")
    app.player1.turn = True
    
    app.playerList = [app.player1, app.AIPlayer] #TODO: kinda don't like this implementation
    app.nonStripedBalls = []
    app.stripedBalls = []

    app.cueStick = cueStickObj(app.cueBall.posX, app.cueBall.posY, app.angle)

    app.playing = True
    app.firstBallPocketed = False
    app.ballTouched = False
    app.scratch = False
    app.gameOver = False

    app.button1 = button(app.width/2, app.height/2, 200, 100)

    # app.cueTestImage = CMUImage("image/cueBall.png", width=100, height=100)


def redrawAll(app):
    drawRect(app.width/2, app.height/2, app.tableWidth + 25, app.tableHeight + 25, fill="brown", align="center")
    drawRect(app.width/2, app.height/2, app.tableWidth, app.tableHeight, fill="steelBlue", align="center")
    for i in range(int(len(app.pockets))):
        drawCircle(app.pockets[i][0], app.pockets[i][1], 12, fill="black")
        drawLabel(i,app.pockets[i][0], app.pockets[i][1], size=15,fill="white")

    # print(ai.ballInPath(app, app.cueBall, (app.blueStriped.posX, app.blueStriped.posY), app.ballList))
    # drawing the ball
    for ball in app.ballList:
        ball.draw()

    #drawing cueStick
    if app.playing and not app.scratch and app.player1.turn:
        app.cueStick.posX = cartToPyX(app.cueBall.posX)
        app.cueStick.posY = cartToPyY(app.cueBall.posY)
        app.cueStick.draw()
    
    gameElements.drawPowerBar(app.width/2, app.height - 35, app.cueStick.distFromBall)

    gameElements.drawPlayerHuds(app.player1, app.AIPlayer)

    if app.gameOver == True:
        drawLabel("GAME OVER", app.width/2, app.height/2, size=60, font="orbitron", bold = True,fill='red')

    # app.button1.drawButtonGraphic("Did it work?")



def testing(ball, pocket):
    """a function for anything being tested"""
    dxBTP = ball.posX - pyToCartX(pocket[0])
    dyBTP = ball.posY - pyToCartY(pocket[1])

    angleToPocket = math.degrees(math.atan2(dyBTP,dxBTP))

    hypoCueX = ball.posX + 2 * ball.r * math.cos(math.radians(angleToPocket))
    hypoCueY = ball.posY + 2 * ball.r * math.sin(math.radians(angleToPocket))

    drawCircle(cartToPyX(hypoCueX), cartToPyY(hypoCueY), 5, fill="purple")
    drawLine(cartToPyX(hypoCueX), cartToPyY(hypoCueY), pocket[0], pocket[1])

def onMouseMove(app, mouseX, mouseY):
    if not app.gameOver:
        if app.player1.turn == True:
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
    if not app.gameOver:
        if app.playing:    
            if app.player1.turn:
                if app.scratch:
                    app.scratch = False
    if app.button1.clicked(mouseX, mouseY):
        print("clicked")

def onKeyPress(app, key):
    if not app.gameOver:
        if app.playing == True:
            if app.player1.turn:
                if key == "s" or key == "down":
                    app.cueStick.addPower(-1)
                if key == "w" or key == "up":
                    app.cueStick.addPower(1)
                if key == "space":
                    app.cueStick.hitCueBall(app.cueBall)
                    app.playing = False
        #For testing:
        # if key == "enter":
        #     if app.scratch:
        #         app.cueBall.setVelo((0,0))
        #         app.cueBall.pocketed = False
        #         if app.cueBall not in app.ballList:
        #             app.ballList.append(app.cueBall)
        #         app.cueBall.posX, app.cueBall.posY, targetBall, targetPocket = ai.scratch(app, app.cueBall, app.ballList, app.pockets, app.AIPlayer.striped)
        #         app.cueStick.setPower(ai.determineBestPower(app.cueBall, targetBall, targetPocket))
        #         app.cueStick.setAngle(ai.determineBestAngle(targetBall, targetPocket, app.cueBall))
        #         app.cueStick.hitCueBall(app.cueBall)
        #         app.scratch = False
        #     else:
        #         ai.hitTheBall(app.cueStick, app.cueBall, app.ballList, app.pockets, app.AIPlayer.striped)
        #     app.playing = False
    

def onKeyHold(app, keys):
    if not app.gameOver:    
        if app.player1.turn:
            if "left" in keys or "a" in keys:
                app.cueStick.addPower(-3)
            if "right" in keys or "d" in keys:
                app.cueStick.addPower(3)

def onStep(app):
    if not app.gameOver:
        if app.playing and app.AIPlayer.turn:
            if app.scratch:
                app.cueBall.setVelo((0,0))
                app.cueBall.pocketed = False
                if app.cueBall not in app.ballList:
                    app.ballList.append(app.cueBall)
                app.cueBall.posX, app.cueBall.posY, targetBall, targetPocket = ai.scratch(app.cueBall, app.ballList, app.pockets, app.AIPlayer.striped)
                app.cueStick.setPower(ai.determineBestPower(app.cueBall, targetBall, targetPocket))
                app.cueStick.setAngle(ai.determineBestAngle(targetBall, targetPocket, app.cueBall))
                app.cueStick.hitCueBall(app.cueBall)
                app.scratch = False
            else:
                ai.hitTheBall(app.cueStick, app.cueBall, app.ballList, app.pockets, app.AIPlayer.striped)
            app.playing = False

        if not app.playing:
            gameElements.checkBallCollisions(app, app.ballList)
            gameElements.checkingPockets(app.ballList, app.pockets, app.stripedBalls, app.nonStripedBalls)

            #If the first ball has been pocketed, the stripe goes to the player
            if not app.firstBallPocketed:
                for ball in app.initalBallList:
                    if not ball.ball8 and not ball.cueBall:
                        if ball.pocketed:
                            app.firstBallPocketed = True
                            for i in range(len(app.playerList)):
                                if app.playerList[i].turn:
                                    app.playerList[i].striped = ball.striped
                                else:
                                    app.playerList[i].striped = not ball.striped
                            break
                
            if gameElements.ballsStopped(app.ballList):
                gameElements.checkWin(app, app.ball8, app.playerList)
                if app.player1.turn: 
                    gameElements.turnLogic(app, app.player1, app.AIPlayer, app.stripedBalls, app.nonStripedBalls, app.ball8, app.cueBall, app.ballTouched)
                else:
                    gameElements.turnLogic(app, app.AIPlayer, app.player1, app.stripedBalls, app.nonStripedBalls, app.ball8, app.cueBall, app.ballTouched)
                app.playing = True  
                app.ballTouched = False

def main():
    runApp()

main()


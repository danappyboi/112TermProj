from cmu_graphics import *
import math
from ballObj import ball
from utilFunctions import*
from cueStick import cueStickObj
import gameElements
from player import player
import ai
import gameSetups
import copy
from button import button
import menu

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

    app.menu = True
    menu.allButtons(app)


def redrawAll(app):
    drawRect(app.width/2, app.height/2, app.tableWidth + 25, app.tableHeight + 25, fill="brown", align="center")
    drawRect(app.width/2, app.height/2, app.tableWidth, app.tableHeight, fill="steelBlue", align="center")
    for i in range(int(len(app.pockets))):
        drawCircle(app.pockets[i][0], app.pockets[i][1], 12, fill="black")
        drawLabel(i,app.pockets[i][0], app.pockets[i][1], size=15,fill="white")

    if not app.menu:
        # drawing the ball
        if not app.paused:
            for ball in app.ballList:
                ball.draw()
        else:
            for ball in app.ballList:
                ball.drawStatic(cartToPyX(ball.posX), cartToPyY(ball.posY))

        #drawing cueStick
        if app.playing and not app.scratch and (app.firstPlayer.turn or (app.secondPlayer.turn and not app.secondPlayer.AI)):
            app.cueStick.posX = cartToPyX(app.cueBall.posX)
            app.cueStick.posY = cartToPyY(app.cueBall.posY)
            app.cueStick.draw()
        
        gameElements.drawPowerBar(app.width/2, app.height - 35, app.cueStick.distFromBall)
        gameElements.drawPlayerHuds(app.firstPlayer, app.secondPlayer)

        #TODO: Make the winner more obvious
        if app.gameOver and not app.menu:
            drawLabel("GAME OVER", app.width/2, app.height/2, size=60, font="orbitron", bold = True,fill='red')

    app.playButton.drawButtonGraphic("Play")
    app.instructionsButton.drawButtonGraphic("Instructions")
    app.optionsButton.drawButtonGraphic("Options")
    app.backButton.drawButtonGraphic("←")
    app.twoPlayerButton.drawButtonGraphic("Two Player")
    app.AIButton.drawButtonGraphic("AI Mode")
    app.pauseButton.drawButtonGraphic("II")
    app.backToMenu.drawButtonGraphic("To Menu")

    menu.draw(app, app.chooseMode, app.instructions, app.options)


def onMouseMove(app, mouseX, mouseY):
    for button in app.buttonList:
        if button.visible and button.clicked(mouseX, mouseY):
            button.highlight = True
        else:
            button.highlight = False
    if not app.menu:
        if not app.gameOver:
            if app.firstPlayer.turn or (app.secondPlayer.turn and not app.secondPlayer.AI):
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

#TODO: maybe instructions during pause?
def onMousePress(app, mouseX, mouseY):
    if app.menu:               
        menu.logic(app, mouseX, mouseY)
    else:
        app.pauseButton.visible = True

        if app.pauseButton.clicked(mouseX, mouseY):
            app.paused = not app.paused
            app.backToMenu.visible = not app.backToMenu.visible

        if app.backToMenu.clicked(mouseX, mouseY):
            app.menu = True
            app.paused = False
            app.backToMenu.visible = False
            app.pauseButton.visible = False

            app.playButton.visible = True
            app.instructionsButton.visible = True
            app.optionsButton.visible = True

        if not (app.gameOver or app.paused):
            if app.playing:    
                if app.firstPlayer.turn or (app.secondPlayer.turn and not app.secondPlayer.AI):
                    if app.scratch:
                        app.scratch = False

def onKeyPress(app, key):
    if not app.menu:
        if key == "p":
            app.paused = not app.paused
            app.backToMenu.visible = not app.backToMenu.visible
        if not (app.gameOver or app.paused):
            if app.playing == True:
                if app.firstPlayer.turn or (app.secondPlayer.turn and not app.secondPlayer.AI):
                    if key == "s" or key == "down":
                        app.cueStick.addPower(-1)
                    if key == "w" or key == "up":
                        app.cueStick.addPower(1)
                    if key == "space":
                        app.cueStick.hitCueBall(app.cueBall)
                        app.playing = False
    

def onKeyHold(app, keys):
    if not app.menu:
        if not (app.gameOver or app.paused):    
            if app.firstPlayer.turn or (app.secondPlayer.turn and not app.secondPlayer.AI):
                if "left" in keys or "a" in keys:
                    app.cueStick.addPower(-3)
                if "right" in keys or "d" in keys:
                    app.cueStick.addPower(3)

def onStep(app):
    if not app.menu:
        if not (app.gameOver or app.paused):
            if app.playing and (app.secondPlayer.turn and app.secondPlayer.AI):
                if app.scratch:
                    app.cueBall.setVelo((0,0))
                    app.cueBall.pocketed = False
                    if app.cueBall not in app.ballList:
                        app.ballList.append(app.cueBall)
                    app.cueBall.posX, app.cueBall.posY, targetBall, targetPocket = ai.scratch(app.cueBall, app.ballList, app.pockets, app.secondPlayer.striped)
                    app.cueStick.setPower(ai.determineBestPower(app.cueBall, targetBall, targetPocket))
                    app.cueStick.setAngle(ai.determineBestAngle(targetBall, targetPocket, app.cueBall))
                    app.cueStick.hitCueBall(app.cueBall)
                    app.scratch = False
                else:
                    ai.hitTheBall(app.cueStick, app.cueBall, app.ballList, app.pockets, app.secondPlayer.striped)
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
                    if app.firstPlayer.turn: 
                        gameElements.turnLogic(app, app.firstPlayer, app.secondPlayer, app.stripedBalls, app.nonStripedBalls, app.ball8, app.cueBall, app.ballTouched)
                    else:
                        gameElements.turnLogic(app, app.secondPlayer, app.firstPlayer, app.stripedBalls, app.nonStripedBalls, app.ball8, app.cueBall, app.ballTouched)
                    app.playing = True  
                    app.ballTouched = False

def main():
    runApp()

main()


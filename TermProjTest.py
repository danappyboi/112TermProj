from cmu_graphics import *
import math
from ballObj import ball

def onAppStart(app):
    app.background = "black"
    app.width = 400
    app.height = 600
    app.tableWidth = 250
    app.tableHeight = 500
    app.pockets = [app.width/2 - app.tableWidth/2, app.height/2 - app.tableHeight/2,
                   app.width/2 + app.tableWidth/2, app.height/2 - app.tableHeight/2,
                   app.width/2 + app.tableWidth/2, app.height/2,
                   app.width/2 + app.tableWidth/2, app.height/2 + app.tableHeight/2,
                   app.width/2 - app.tableWidth/2, app.height/2 + app.tableHeight/2,
                   app.width/2- app.tableWidth/2, app.height/2]
    app.angle = 180
    # app.stepsPerSecond = 10

    app.oldtick = 0
    app.tick = 1
    app.runStep = False

    app.redBall = ball(app.width/2, app.height/2 - 200, "red", velo=(0,0))
    app.blueBall = ball(app.width/2 - 18, app.height/2 - 200, "blue", velo=(0,0))
    app.greenBall = ball(app.width/2 - 18 * 2, app.height/2 - 200, "lime", velo=(0,0))
    app.orangeBall = ball(app.width/2 - 18 * 3, app.height/2 - 200, "orange", velo=(0,0))
    app.yellowBall = ball(app.width/2 + 18, app.height/2 -200, "yellow", velo=(0,0))
    app.blackBall = ball(app.width/2 + 18 * 2, app.height/2 -200, "black", velo=(0,0))
    app.purpleBall = ball(app.width/2 - 18 * 1.5, app.height/2 - 200 + 18, "purple", velo=(0,0))
    app.pinkBall = ball(app.width/2 - 18 * 0.5, app.height/2 - 200 + 18, "pink", velo=(0,0))
    app.grayBall = ball(app.width/2 + 18 * 1.5, app.height/2 - 200 + 18, "gray", velo=(0,0))
    app.lightBall = ball(app.width/2 + 18 * .5, app.height/2 - 200 + 18, "lightBlue", velo=(0,0))

    app.ball1 = ball(app.width/2 + 18, app.height/2 - 200 + 18 * 2, 'mediumVioletRed', velo=(0,0))
    app.ball2 = ball(app.width/2 - 18, app.height/2 - 200 + 18 * 2, 'brown', velo=(0,0))
    app.ball3 = ball(app.width/2, app.height/2 - 200 + 18 * 2, 'darkSlateGray', velo=(0,0))
    app.ball4 = ball(app.width/2 - 18 * .5, app.height/2 - 200 + 18 * 3, 'fireBrick', velo=(0,0))
    app.ball5 = ball(app.width/2 + 18 * .5, app.height/2 - 200 + 18 * 3, 'gold', velo=(0,0))
    app.ball6 = ball(app.width/2, app.height/2 - 200 + 18 * 4, 'darkTurquoise', velo=(0,0))

    app.cueBall = ball(app.width/2, app.height/2 + 100, "white", velo=(0,0))

    app.ballList = [app.cueBall, app.redBall, app.blueBall, app.greenBall, 
                    app.yellowBall, app.blackBall, app.purpleBall, app.pinkBall, 
                    app.grayBall, app.lightBall, app.ball1, app.ball2,
                    app.ball3, app.ball4, app.ball5, app.ball6]


def drawStick(posX, posY, angle, distFromBall):
    mathAngle = angle + 270
    stickSize = 300
    if not(angle % 360 < 90 or angle % 360 > 270):
        posY -= (stickSize + distFromBall) * math.sin(math.radians(mathAngle))
    else:
        posY -= distFromBall * math.sin(math.radians(mathAngle))

    drawRect(posX - ((stickSize)/2 + distFromBall)* math.cos(math.radians(mathAngle)), posY,
        8, stickSize, fill=gradient("tan", "brown", start="top"), align="top", 
        rotateAngle = angle)

def distance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5

def checkBallCollisions(app):
    for i in range(len(app.ballList)):
        for j in range(i, len(app.ballList)):
            if i == j:
                continue
            ball1 = app.ballList[i]
            ball2 = app.ballList[j]

            if distance(ball1.posX, ball1.posY, ball2.posX, ball2.posY) <= (ball1.r + ball2.r):
                # print("titties")

                if distance(ball1.posX, ball1.posY, ball2.posX, ball2.posY) < (ball1.r + ball2.r):
                    ball1.posX -= 20
                    ball1.posY -= 20
                    print("HERE!!")

                ogVector = ball1.getVeloVector()
                ogAngle = ball1.getVeloAngle()
                angleDiff = math.degrees(math.atan2((ball2.velo[1] - ball1.velo[1]),(ball2.velo[0] - ball1.velo[0])))
                ball1.setVeloVector(ogVector * math.sin(ogAngle), angleDiff + ogAngle)
                ball2.setVeloVector(ogVector * math.cos(ogAngle), angleDiff + ogAngle)

                print(f"ogVector: {ogVector}")
                print(f"ogAngle: {ogAngle}")
                print(f"angleDiff: {angleDiff}\n")



def redrawAll(app):
    drawRect(app.width/2, app.height/2, app.tableWidth + 25, app.tableHeight + 25, fill="brown", align="center")
    drawRect(app.width/2, app.height/2, app.tableWidth, app.tableHeight, fill="green", align="center")
    for i in range(int(len(app.pockets)/2)):
        drawCircle(app.pockets[i * 2], app.pockets[i * 2 + 1], 10, fill="black")

    # drawing the ball
    for ball in app.ballList:
        ball.draw()

    drawStick(app.cueBall.posX, app.cueBall.posY, app.angle, 40)




def onMouseMove(app, mouseX, mouseY):
    posX = app.width/2
    posY = app.height/2
    app.angle = math.degrees(math.atan2(mouseY - posY, mouseX - posX)) - 90
    
# def onKeyPress(app, key):
#     if key == "up":
#         app.cueBall.posY -= 5
#     if key == "down":
#         app.cueBall.posY += 5
#     if key == "left":
#         app.cueBall.posX -= 5
#     if key == "right":
#         app.cueBall.posX += 5
#     if key == "s":
#         takeStep(app)
#     pass

# def onKeyHold(app, keys):
#     # if "up" in keys:
#     #     app.cueBall.posY -= 5
#     # if "down" in keys:
#     #     app.cueBall.posY += 5
#     # if "left" in keys:
#     #     app.cueBall.posX -= 5
#     # if "right" in keys:
#     #     app.cueBall.posX += 5
#     pass

# def takeStep(app):
#     checkBallCollisions(app)
    
#     # pass
def onStep(app):
    app.tick +=1
    

def main():
    runApp()

main()


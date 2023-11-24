from cmu_graphics import *
import math
from ballObj import ball
from matrixOps import rotateAlgo, revertAlgo
import pointConvert

def onAppStart(app):
    app.background = "black"
    app.width = 600
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

    app.redBall = ball(0, 0 + 200, "red", velo=(0,0))
    app.cueBall = ball(12,0 - 100, "white", velo=(0, 8))

    app.ballList = [app.cueBall, app.redBall]


#TODO: because im chaning position, this is also probably fucked up, gotta fixxx
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

            dx = abs(ball1.posX-ball2.posX)
            dy = abs(ball1.posY-ball2.posY)
            angle = math.atan2(dy,dx)

            # if ball1.getVeloAngle() - angle > ball2.getVeloAngle() - angle:
            #     ball1, ball2 = ball2, ball1
            

            distanceBetweenBalls = distance(ball1.posX, ball1.posY, ball2.posX, ball2.posY) 
            if distanceBetweenBalls <= (ball1.r + ball2.r):
                # print("titties")

                # # putting them back
                if distanceBetweenBalls < (ball1.r + ball2.r):
                    if ball1.velo[0] > 0:
                        ball1.posX += (distanceBetweenBalls - (ball1.r + ball2.r))
                    else:
                        ball1.posX -= (distanceBetweenBalls - (ball1.r + ball2.r)) 

                    if ball1.velo[1] > 0:
                        ball1.posY += (distanceBetweenBalls - (ball1.r + ball2.r))
                    else:
                        ball1.posY -= (distanceBetweenBalls - (ball1.r + ball2.r))
                    print("HERE!!")

                dx = abs(ball1.posX-ball2.posX)
                dy = abs(ball1.posY-ball2.posY)
                angle = math.atan2(dy,dx)

                # #Weird vid code
                # ###
                # ball1.velo = rotateAlgo(ball1.velo, angle)
                # ball2.velo = rotateAlgo(ball2.velo, angle)

                # if distanceBetweenBalls < (ball1.r + ball2.r):
                #     if ball1.velo[0] != 0:
                #         ball1.posX += (ball1.velo[0]/abs(ball1.velo[0])) * distanceBetweenBalls/2
                #     if ball2.velo[0] != 0:
                #         ball2.posX += (ball2.velo[0]/abs(ball2.velo[0])) * distanceBetweenBalls/2

                # tempVelo = ball1.velo
                # ball1.setVelo(ball2.velo)
                # ball2.setVelo(tempVelo)

                # ball1.velo = revertAlgo(ball1.velo, angle)
                # ball2.velo = revertAlgo(ball2.velo, angle)
                # ###

                # this is my code, most of it is probably dogshit
                ogVector = ball1.getVeloVector()
                ogAngle = ball1.getVeloAngle()
                # angleDiff = math.degrees(math.atan2((ball2.velo[1] - ball1.velo[1]),(ball2.velo[0] - ball1.velo[0])))
                ball1.setVeloVector(ogVector * math.sin(90-angle), 180-(90 + angle))
                ball2.setVeloVector(ogVector * math.cos(90-angle) + ball2.getVeloVector(), 90 + angle)

                # print(f"ogVector: {ogVector}")
                # print(f"ogAngle: {ogAngle}")
                # print(f"angleDiff: {angleDiff}\n")



def redrawAll(app):
    drawRect(app.width/2, app.height/2, app.tableWidth + 25, app.tableHeight + 25, fill="brown", align="center")
    drawRect(app.width/2, app.height/2, app.tableWidth, app.tableHeight, fill="green", align="center")
    for i in range(int(len(app.pockets)/2)):
        drawCircle(app.pockets[i * 2], app.pockets[i * 2 + 1], 10, fill="black")

    # drawing the ball
    for ball in app.ballList:
        ball.draw()
    
    testingNotes(app, app.ballList)

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



# def onMouseMove(app, mouseX, mouseY):
#     # posX = app.width/2
#     # posY = app.height/2
#     # app.angle = math.degrees(math.atan2(mouseY - posY, mouseX - posX)) - 90
#     pass

# def onKeyPress(app, key):
    # if key == "up":
    #     app.cueBall.posY -= 5
    # if key == "down":
    #     app.cueBall.posY += 5
    # if key == "left":
    #     app.cueBall.posX -= 5
    # if key == "right":
    #     app.cueBall.posX += 5
    # if key == "s":
    #     takeStep(app)
    # pass

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

def onStep(app):
    checkBallCollisions(app)
    

def main():
    runApp()

main()


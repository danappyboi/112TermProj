from cmu_graphics import *
import math
from ballObj import ball
from matrixOps import rotateAlgo, revertAlgo, dot, dotScalar, add
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

    #TODO: fix whatever tf happens here
    # app.redBall = ball(0, 0 + 200, "red", velo=(0,0))
    # app.cueBall = ball(8,0 - 100, "white", velo=(0, 10))

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

    app.cueBall = ball(0, 0 - 100, "lightGrey", velo=(0,12))

    app.ballList = [app.cueBall, app.redBall, app.blueBall, app.greenBall, 
                    app.yellowBall, app.blackBall, app.purpleBall, app.pinkBall, 
                    app.grayBall, app.lightBall, app.ball1, app.ball2,
                    app.ball3, app.ball4, app.ball5, app.ball6]

    # app.redBall = ball(0, 0 + 200, "red", velo=(0,0))
    # app.cueBall = ball(0,0 - 100, "lightGrey", velo=(0, 12))

    # app.ballList = [app.cueBall, app.redBall]


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
           

            distanceBetweenBalls = distance(ball1.posX, ball1.posY, ball2.posX, ball2.posY) 
            if distanceBetweenBalls <= (ball1.r + ball2.r):
                # print("titties")

                # putting them back
                if distanceBetweenBalls < (ball1.r + ball2.r):
                    if ball1.velo[0] > 0:
                        ball1.posX += (distanceBetweenBalls - (ball1.r + ball2.r))
                    else:
                        ball1.posX -= (distanceBetweenBalls - (ball1.r + ball2.r)) 

                    if ball1.velo[1] > 0:
                        ball1.posY += (distanceBetweenBalls - (ball1.r + ball2.r))
                    else:
                        ball1.posY -= (distanceBetweenBalls - (ball1.r + ball2.r))

                # if distanceBetweenBalls < (ball1.r + ball2.r):
                #     if ball1.velo[0] != 0:
                #         ball1.posX += (ball1.velo[0]/abs(ball1.velo[0])) * distanceBetweenBalls/2
                #     if ball2.velo[0] != 0:
                #         ball2.posX += (ball2.velo[0]/abs(ball2.velo[0])) * distanceBetweenBalls/2

                dx = abs(ball1.posX-ball2.posX)
                dy = abs(ball1.posY-ball2.posY)
                angle = math.degrees(math.atan2(dy,dx))
                print(angle)

                #normal vector
                n = (ball2.posX-ball1.posX, ball2.posY-ball1.posY)
                
                #unit normal vector
                magN = math.sqrt(n[0]**2+n[1]**2)
                un = (n[0]/magN, n[1]/magN)

                #unit tangent vector
                ut = (-un[1], un[0])

                v1n = dot(un, ball1.velo)
                v1t = dot(ut, ball1.velo)
                v2n = dot(un, ball2.velo)
                v2t = dot(ut, ball2.velo)

                v1tNew = v1t
                v2tNew = v2t
                v1nNew = v2n
                v2nNew = v1n

                v1nVec = dotScalar(v1nNew, un)
                v1tVec = dotScalar(v1tNew, ut)
                v2nVec = dotScalar(v2nNew, un)
                v2tVec = dotScalar(v2tNew, ut)

                ball1.velo = add(v1nVec, v1tVec)
                ball2.velo = add(v2nVec, v2tVec)

                # this is my code, most of it is probably dogshit
                # ogVector = ball1.getVeloVector()
                # ball1.setVeloVector(ogVector * math.sin(90-angle), 180-(90 + angle))
                # ball2.setVeloVector(ogVector * math.cos(90-angle) + ball2.getVeloVector(), 180-angle)



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


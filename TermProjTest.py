from cmu_graphics import *
import math
from ballObj import ball
from matrixOps import*
from pointConvert import*
from cueStick import cueStickObj

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
    app.cueBall = ball(0,0 - 100, "lightGrey", velo=(0, 12))
    app.ballList = [app.cueBall, app.redBall]

    app.cueStick = cueStickObj(app.cueBall.posX, app.cueBall.posY, app.angle)
                    #cueStickObj(app.cueBall.posX, app.cueBall.posY, app.angle)


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

                # if distanceBetweenBalls < (ball1.r + ball2.r):
                #     if ball1.velo[0] != 0:
                #         ball1.posX += (ball1.velo[0]/abs(ball1.velo[0])) * distanceBetweenBalls/2
                #     if ball2.velo[0] != 0:
                #         ball2.posX += (ball2.velo[0]/abs(ball2.velo[0])) * distanceBetweenBalls/2


                #dont even ask me how this shit works, peep this https://www.vobarian.com/collisions/2dcollisions2.pdf 

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

# def moveBallBack(app):
#     i = 0
#     while i < len(app.ballList):
#         for j in range(i, len(app.ballList)):

def redrawAll(app):
    drawRect(app.width/2, app.height/2, app.tableWidth + 25, app.tableHeight + 25, fill="brown", align="center")
    drawRect(app.width/2, app.height/2, app.tableWidth, app.tableHeight, fill="green", align="center")
    for i in range(int(len(app.pockets)/2)):
        drawCircle(app.pockets[i * 2], app.pockets[i * 2 + 1], 10, fill="black")

    # drawing the ball
    for ball in app.ballList:
        ball.draw()

    app.cueStick.draw()
    # print(app.cueStick.posX, app.cueStick.posY)
    # drawStick(app.cueBall.posX, app.cueBall.posY, app.angle, 10)
    
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
    app.angle = math.degrees(math.atan2(mouseY - cartToPyY(posY), mouseX - cartToPyX(posX))) - 90
    app.cueStick.posX = cartToPyX(posX)
    app.cueStick.posY = cartToPyY(posY)
    app.cueStick.angle = app.angle
    # print(f"angle: {app.angle}")
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


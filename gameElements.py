import math
from cmu_graphics import*
from ballObj import ball #do I really not need this?
from matrixOps import*


def distance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5

def checkBallCollisions(ballList):
    """The function that does all the math for the ball collisions"""
    for i in range(len(ballList)):
        for j in range(i, len(ballList)):
            if i == j:
                continue
            
            ball1 = ballList[i]
            ball2 = ballList[j]
           

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
#     while i < len(ballList):
#         for j in range(i, len(ballList)):
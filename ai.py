from cmu_graphics import*
import math
from utilFunctions import*
from cueStick import cueStickObj
from gameElements import setVeloAfterCollision
import copy
import sys
# import ballObj #would have done it the other way, but it makes writing code easier

#TODO: think you could animate the way it moves?
def hitTheBall(cueStick, cueBall, power, angle):
    cueStick.setPower(power)
    cueStick.angle(angle) #not done
    cueStick.hitCueBall(cueBall)



#TODO: really basic rn
def determineBestBall(cueBall, ballList, striped):
    possibleBallsAndPockets = []

    for ball in ballList:
        if ball.legal(striped):
            if not ballInPath(cueBall, ball, ballList):
                possibleBallsAndPockets.append(ball)
    
    #just hit the first legal ball
    if possibleBallsAndPockets == []:
        for ball in ballList:
            if ball.legal(striped):
                return ball
    else:
        #hit the first possible good hit
        return possibleBallsAndPockets[0]



#TODO: is it safe to assume the ball isnt moving?
def determineBestAngle(ball, pocket, cueBall):
    """For a given ball, this function returns the best angle and velocity for 
        the cueBall to be shot at in order to the ball to be pocketed into a given
        pocket."""

    dxBTP = ball.posX - pyToCartX(pocket[0])
    dyBTP = ball.posY - pyToCartY(pocket[1])

    angleToPocket = math.degrees(math.atan2(dyBTP,dxBTP))

    hypoCueX = ball.posX + 2 * ball.r * math.cos(math.radians(angleToPocket))
    hypoCueY = ball.posY + 2 * ball.r * math.sin(math.radians(angleToPocket))

    angleHypoCueToCue = math.degrees(math.atan2(cueBall.posY - hypoCueY,
                                                cueBall.posX - hypoCueX))
    return angleHypoCueToCue

def determineBestMagnitude(cueBall, ball, pocket):
    """Returns a magnitude for a given ball and pocket."""
    distBTP = distance(ball.posX, ball.posY, pyToCartX(pocket[0]), pyToCartY(pocket[1]))
    distBTC = distance(cueBall.posX, cueBall.posY, ball.posX, ball.posY)

    val = 2 * ((distBTC + distBTP)/47.5 + 2) 
    #literally no rhyme or reason for this value, 
    #just works well enough
    return val

def ballInPath(cueBall, targetBall, ballList):
    """Determines whether or not a ball is in the path of the cueBall 
        and a given targetBall"""
    for ball in ballList:
        if (ball != targetBall) and (ball != cueBall):
            perpPoint = perpendPointOnLine(cueBall, targetBall, ball)
            if distance(ball.posX, ball.posY, perpPoint[0], perpPoint[1]) <= 2* ball.r:
                return True
    return False

def perpendPointOnLine(cueBall, targetBall, ball):
    """Finds the point that creates a line perpendicular to the line
    created by the targetBall and cueBall that goes through the ball."""
    dx = targetBall.posX - cueBall.posX
    dy = targetBall.posY - cueBall.posY

    if dx == 0:
        slope = dy/100000
    else:
        slope = dy/dx

    if slope == 0:
        invSlope = 1/100000
    else:
        invSlope = 1/slope

    invMat = [[slope/(slope**2+1), -slope/(slope**2+1)],
              [-1/(slope**2+1), -(slope**2)/(slope**2+1)]]
    bVec = [-targetBall.posY+slope*targetBall.posX, 
            -ball.posY + -(invSlope)*ball.posX]
    
    pointX = (invMat[0][0] * bVec[0] + invMat[0][1] * bVec[1])
    pointY = (invMat[1][0] * bVec[0] + invMat[1][1] * bVec[1])
    return (pointX, pointY)







    
    
        


        



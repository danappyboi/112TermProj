from cmu_graphics import*
import math
from utilFunctions import*
from cueStick import cueStickObj
from gameElements import setVeloAfterCollision
import copy
import sys
# import ballObj #would have done it the other way, but it makes writing code easier

#TODO: think you could animate the way it moves?
def hitTheBall(cueStick, cueBall, ballList, pocketList, striped):
    #TODO: targetBall and targetPocket are redunant
    targetBall, targetPocket, angle, power = determineBestBall(cueBall, ballList, pocketList, striped)
    cueStick.setPower(power)
    cueStick.setAngle(angle)
    cueStick.hitCueBall(cueBall)

#TODO: really basic rn
def determineBestBall(cueBall, ballList, pocketList, striped):
    bestShots = []

    for ball in ballList: 
        if ball.legal(striped):
            if not ballInPath(cueBall, ball, ballList):
                for pocket in pocketList:
                    angle = determineBestAngle(ball, pocket, cueBall)
                    print(f"angle in dbb: {angle} {possibleAngle(ball, cueBall, angle)}")
                    if possibleAngle(ball, cueBall, angle):
                        bestShots.append((ball, pocket, angle, determineBestPower(cueBall, ball, pocket)))
    
    #just hit the first legal ball
    if bestShots == []:
        for ball in ballList:
            if ball.legal(striped):
                print("shit.")
                return (ball, pocketList[0], determineBestAngle(ball, pocketList[0], cueBall), 
                        determineBestPower(cueBall, ball, pocketList[0]))
    else:
        #hit the first possible good hit
        print("not shit")
        return bestShots[0]

def possibleAngle(ball, cueBall, angle):
    """Returns if the angle provided is possible for the cueBall to make."""
    dxBTC = ball.posX - cueBall.posX
    dyBTC = ball.posY - cueBall.posY

    angleBTC = math.atan2(dyBTC, dxBTC)
    pos1 = revertAlgo((0, 2 * ball.r), angleBTC)
    pos2 = revertAlgo((0, -2*ball.r), angleBTC)
    pos1 = add(pos1, (ball.posX, ball.posY))
    pos2 = add(pos2, (ball.posX, ball.posY))

    buffer = 1
    """Buffer angle to make sure it doesn't take crazy 90° shots"""
    dxCTPos1 = cueBall.posX - pos1[0]
    dyCTPos1 = cueBall.posY - pos1[1]
    angle1 = math.degrees(math.atan2(dyCTPos1, dxCTPos1))
    dxCTPos2 = cueBall.posX - pos2[0]
    dyCTPos2 = cueBall.posY - pos2[1]
    angle2 = math.degrees(math.atan2(dyCTPos2, dxCTPos2))

    print(f"angles in question: {angle1} {angle2}")
    #TODO: hopefully angle1 and 2 shouldn't be flipped
    return angleInRange(angle, angle2 + buffer, angle1 - buffer) #hopefully angle1 and 2 shouldn't be flipped

    # return (cartToPyX(pos1[0]), cartToPyY(pos1[1])), (cartToPyX(pos2[0]), cartToPyY(pos2[1]))

#just wanted a quick and simple solution https://stackoverflow.com/questions/66799475/how-to-elegantly-find-if-an-angle-is-between-a-range
def angleInRange(alpha, lower, upper):
    return (alpha - lower) % 360 <= (upper - lower) % 360


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

def determineBestPower(cueBall, ball, pocket):
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







    
    
        


        



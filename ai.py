from cmu_graphics import*
import math
from utilFunctions import*
# import ballObj #would have done it the other way, but it makes writing code easier

#TODO: still lk kinda inaccurate
#TODO: account for balls inbetween target and pocket

#TODO: think you could animate the way it moves?
def hitTheBall(cueStick, cueBall, ballList, pocketList, striped):
    """Hits the ball based on the determineBestBall function."""
    #TODO: targetBall and targetPocket are redunant
    targetBall, targetPocket, angle, power = determineBestBall(cueBall, ballList, pocketList, striped)
    cueStick.setPower(power)
    cueStick.setAngle(angle)
    cueStick.hitCueBall(cueBall)
    # print(f"firing at: {pocketList.index(targetPocket)}")

#TODO: really basic rn
def determineBestBall(cueBall, ballList, pocketList, striped):
    """Determines the best ball and angle to hit based on the position of the cueBall and the options."""
    bestShots = []

    for ball in ballList: 
        if ball.legal(striped):
            for pocket in pocketList:
                dxBTP = ball.posX - pyToCartX(pocket[0])
                dyBTP = ball.posY - pyToCartY(pocket[1])

                angleToPocket = math.degrees(math.atan2(dyBTP,dxBTP))

                """hypoCue represents the position of the best ball placement based on the pocket"""
                hypoCueX = ball.posX + 2 * ball.r * math.cos(math.radians(angleToPocket))
                hypoCueY = ball.posY + 2 * ball.r * math.sin(math.radians(angleToPocket))

                targetPoint = (hypoCueX, hypoCueY)
                pocketPoint = (pyToCartX(pocket[0]), pyToCartY(pocket[1]))

                """Just a bunch of checks to make sure this is a possible shot."""
                if cueBallInPosition(cueBall, targetPoint, pocket):
                    #TODO: i dont think the second one is working
                    if not ballInPath(cueBall, targetPoint, ballList) and not ballInPath(ball, pocketPoint, ballList):
                        angle = determineBestAngle(ball, pocket, cueBall)
                        if possibleAngle(ball, cueBall, angle):
                            bestShots.append((ball, pocket, angle, determineBestPower(cueBall, ball, pocket)))

    if bestShots == []:
        if only8BallLeft(ballList, striped) != False:
            ball8 = only8BallLeft(ballList, striped)
            for pocket in pocketList:
                dx8TP = ball8.posX - pyToCartX(pocket[0])
                dy8TP = ball8.posY - pyToCartY(pocket[1])

                angleToPocket = math.degrees(math.atan2(dy8TP,dx8TP))

                """hypoCue represents the position of the best ball placement based on the pocket"""
                hypoCueX = ball8.posX + 2 * ball8.r * math.cos(math.radians(angleToPocket))
                hypoCueY = ball8.posY + 2 * ball8.r * math.sin(math.radians(angleToPocket))

                targetPoint = (hypoCueX, hypoCueY)
                pocketPoint = (pyToCartX(pocket[0]), pyToCartY(pocket[1]))

                if cueBallInPosition(cueBall, targetPoint, pocket):
                    #TODO: i dont think the second one is working
                        if not ballInPath(cueBall, targetPoint, ballList) and not ballInPath(ball8, pocketPoint, ballList):
                            angle = determineBestAngle(ball8, pocket, cueBall)
                            if possibleAngle(ball8, cueBall, angle):
                                bestShots.append((ball8, pocket, angle, determineBestPower(cueBall, ball8, pocket)))

    
    """If there's no good shots, just hit the first ball in the ballList."""
    if bestShots == []:
        for ball in ballList:
            if ball.legal(striped):
                print("shit.") #tests for me
                return (ball, pocketList[0], determineBestAngle(ball, pocketList[0], cueBall), 
                        determineBestPower(cueBall, ball, pocketList[0]))
    else:
        print("not shit") #tests for me
        bestAngle = 0
        bestShot = 0
        """Out of the best shots, pick the shot that is the closest to just hitting the ball straight on."""
        for shot in bestShots:
            angle = shot[2]
            ball = shot[0]
            dyCTB = cueBall.posY - ball.posY
            dxCTB = cueBall.posX - ball.posX
            straightAngle = math.degrees(math.atan2(dyCTB, dxCTB))
            if abs(angleDiff(angle, straightAngle)) < abs(angleDiff(bestAngle, straightAngle)):
                bestAngle = angle
                bestShot = shot
                
        return bestShot

def only8BallLeft(ballList, striped):
    for ball in ballList:
        if ball.legal(striped):
            return False
    for i in range(len(ballList)):
        if ballList[i].ball8:
            return ballList[i]


def scratch(app, cueBall, ballList, pocketList, striped):
    """Returns new cueBall positions and the angle and ball to aim for after a scratch. 
        Just picks the first shot that is straight on from a specfic distance away."""
    bigFlag = False
    for ball in ballList:
        if ball.legal(striped):
            for pocket in pocketList:

                dxBTP = ball.posX - pyToCartX(pocket[0])
                dyBTP = ball.posY - pyToCartY(pocket[1])

                angleToPocket = math.degrees(math.atan2(dyBTP,dxBTP))

                preferredDistToCue = 10
                """Where the cueBall will hypothetically be at the shot."""
                hypoCueX = ball.posX + ((2 * ball.r) + preferredDistToCue) * math.cos(math.radians(angleToPocket))
                hypoCueY = ball.posY + ((2 * ball.r) + preferredDistToCue) * math.sin(math.radians(angleToPocket))

                if not ballInPath(cueBall, (hypoCueX, hypoCueY), ballList) and not ballInPath(ball, (pocket[0], pocket[1]), ballList):
                    """Making sure there isn't a ball in hypoCue position."""
                    flag = False
                    for otherBall in ballList:
                        if ball == otherBall or ball.cueBall:
                            continue
                        if distance(otherBall.posX, otherBall.posY, hypoCueX, hypoCueY) < 2*ball.r:
                            flag = True
                            break
                    if flag == False:
                        return (hypoCueX, hypoCueY, ball, pocket)
        if bigFlag == True:
            break
    """If we went through every possible ball and pocket and didn't find a shot, just shoot 
        at the first ball at the 0th hole from (0,0)."""
    if bigFlag == False:
        print("whoops")
        return (0, 0, ballList[0], pocketList[0])


def cueBallInPosition(cueBall, targetPoint, pocket):
    """Checking to make sure the cueBall is in a position to actually hit the ball at the pocket."""

    minX = min(targetPoint[0], pyToCartX(pocket[0]))
    maxX = max(targetPoint[0], pyToCartX(pocket[0]))
    minY = min(targetPoint[1], pyToCartY(pocket[1]))
    maxY = max(targetPoint[1], pyToCartY(pocket[1]))

    """The cueBall has to be behind the target in order to shoot it, if its anywhere in front, its 
        a terrible shot."""
    if (minX < cueBall.posX < maxX) or (minY < cueBall.posY < maxY):
        return False
    return True

def possibleAngle(ball, cueBall, angle):
    """Returns if the angle provided is possible for the cueBall to make."""
    dxBTC = ball.posX - cueBall.posX
    dyBTC = ball.posY - cueBall.posY

    angleBTC = math.atan2(dyBTC, dxBTC)

    """Using Lin Alg, find the points where the cueBall would juuuuust graze the 
        target."""
    pos1 = revertAlgo((0, 2 * ball.r), angleBTC)
    pos2 = revertAlgo((0, -2*ball.r), angleBTC)
    pos1 = add(pos1, (ball.posX, ball.posY))
    pos2 = add(pos2, (ball.posX, ball.posY))

    """Buffer angle to make sure it doesn't take crazy 90° shots"""
    buffer = 1
    
    dxCTPos1 = cueBall.posX - pos1[0]
    dyCTPos1 = cueBall.posY - pos1[1]
    angle1 = math.degrees(math.atan2(dyCTPos1, dxCTPos1))
    dxCTPos2 = cueBall.posX - pos2[0]
    dyCTPos2 = cueBall.posY - pos2[1]
    angle2 = math.degrees(math.atan2(dyCTPos2, dxCTPos2))

    """angle1 and angle2 are the angle the cueBall would have to take to make
        the crazy shots. If the ball isn't in the range of grazing the ball, 
        its definitely not a good shot."""
    return angleInRange(angle, angle2 + buffer, angle1 - buffer) #hopefully angle1 and 2 shouldn't be flipped

#just wanted a quick and simple solution https://stackoverflow.com/questions/66799475/how-to-elegantly-find-if-an-angle-is-between-a-range
def angleInRange(alpha, lower, upper):
    return (alpha - lower) % 360 <= (upper - lower) % 360

#another one https://stackoverflow.com/questions/1878907/how-can-i-find-the-smallest-difference-between-two-angles-around-a-point 
def angleDiff(angle1, angle2):
    a = angle1 - angle2
    return (a + 180) % 360 - 180


def determineBestAngle(ball, pocket, cueBall):
    """For a given ball, this function returns the best angle and velocity for 
        the cueBall to be shot at in order to the ball to be pocketed into a given
        pocket."""

    dxBTP = ball.posX - pyToCartX(pocket[0])
    dyBTP = ball.posY - pyToCartY(pocket[1])

    angleToPocket = math.degrees(math.atan2(dyBTP,dxBTP))

    """hypoCue is the ideal position for the cueBall to collide with the ball at."""
    hypoCueX = ball.posX + 2 * ball.r * math.cos(math.radians(angleToPocket))
    hypoCueY = ball.posY + 2 * ball.r * math.sin(math.radians(angleToPocket))

    """Just return the angle the cueBall needs to take to get to hypoCue."""
    angleHypoCueToCue = math.degrees(math.atan2(cueBall.posY - hypoCueY,
                                                cueBall.posX - hypoCueX))
    return angleHypoCueToCue

def determineBestPower(cueBall, ball, pocket):
    """Returns a magnitude for a given ball and pocket."""
    distBTP = distance(ball.posX, ball.posY, pyToCartX(pocket[0]), pyToCartY(pocket[1]))
    distBTC = distance(cueBall.posX, cueBall.posY, ball.posX, ball.posY)

    #TODO: gotta make it make sense
    """literally no rhyme or reason for this value, just works well enough"""
    val = 2 * ((distBTC + distBTP)/47.5 + 2) 

    return val

def ballInPath(cueBall, targetPoint, ballList):
    """Determines whether or not a ball is in the path of the cueBall 
        and a given targetPoint"""
    for ball in ballList:
        if (ball != cueBall) and not (ball.posX == targetPoint[0] and ball.posY == targetPoint[1]):
            perpPoint = perpendPointOnLine(cueBall, targetPoint, ball)
            """First, check if the ball is in the line of shot, if it does,
                check that its ACTUALLY in the line of the shot, and not 
                behind it."""
            if distance(ball.posX, ball.posY, perpPoint[0], perpPoint[1]) < 2* (ball.r + 2): #the two is for buffer
                minBallX = min(targetPoint[0], cueBall.posX)
                maxBallX = max(targetPoint[0], cueBall.posX)
                minBallY = min(targetPoint[1], cueBall.posY)
                maxBallY = max(targetPoint[1], cueBall.posY)
                
                if (minBallX <= ball.posX <= maxBallX) and (minBallY <= ball.posY <= maxBallY):
                    return True
    return False

def perpendPointOnLine(cueBall, targetPoint, ball):
    """Finds the point that creates a line perpendicular to the line
    created by the targetBall and cueBall that goes through the ball."""
    dx = targetPoint[0] - cueBall.posX
    dy = targetPoint[1] - cueBall.posY

    if dx == 0:
        slope = dy/100000
    else:
        slope = dy/dx

    if slope == 0:
        invSlope = 1/100000
    else:
        invSlope = 1/slope

    """The cueBall to targetPoint creates a line, and we want to find the
    perpendicular line that goes through the ball. This is basically a algebra
    1 problem with two equations, meaning we can chuck the slopes of the equations
    into a matrix. 
    [  slope     -1][ x ] = [b1]
    [-1/slope    -1][ y ] = [b2]  

    Using https://matrixcalc.org/ to find the inverse, we can find the x and y
    coords of point that makes a perpendicular line that goes through the ball.
    """
    invMat = [[slope/(slope**2+1), -slope/(slope**2+1)],
              [-1/(slope**2+1), -(slope**2)/(slope**2+1)]]
    bVec = [-targetPoint[1]+slope*targetPoint[0], 
            -ball.posY + (-invSlope)*ball.posX]
    
    pointX = (invMat[0][0] * bVec[0] + invMat[0][1] * bVec[1])
    pointY = (invMat[1][0] * bVec[0] + invMat[1][1] * bVec[1])
    return (pointX, pointY)







    
    
        


        



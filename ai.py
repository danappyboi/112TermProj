from cmu_graphics import*
import math
from utilFunctions import*
from cueStick import cueStickObj
import copy
from gameElements import setVeloAfterCollision
# import ballObj #would have done it the other way, but it makes writing code easier

#TODO: think you could animate the way it moves?
def hitTheBall(cueStick, cueBall, power, angle):
    cueStick.setPower(power)
    cueStick.angle(angle) #not done
    cueStick.hitCueBall(cueBall)


#TODO: what about the velocity?
#TODO: is it safe to assume the ball isnt moving?
def determineBestAngle(ball, pocket, cueBall, ballList):
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



    




    
    
        


        



import math
from cmu_graphics import*
from ballObj import ball #do I really not need this?
from matrixOps import*
from pointConvert import*
import copy

width = 600
height = 600
tableWidth = 225
tableHeight = 450

def distance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5

#TODO: get a better understanding of this
def checkBallCollisions(ballList):
    """The function that does all the math for the ball collisions and sets the velocities."""
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

def drawPowerBar(x, y, power):
    """Draws the power bar at the bottom of the screen."""
    barWidth = 200
    barHeight = 30
    drawRect(x, y, barWidth, barHeight, border="white", align="center")
    drawLine(x - barWidth/2 +2, y, x-barWidth/2 + barWidth *(power/100), y, fill="red", lineWidth=barHeight-5, dashes=True)

def checkingPockets(ballList, pocketList, stripedList, nonStripedList):
    """Checks if any balls have been pocketed and places them in the correct player's pocketed list."""
    for ball in ballList:
        for pocket in pocketList:
            if distance(cartToPyX(ball.posX), cartToPyY(ball.posY), pocket[0], pocket[1]) < 10:
                ball.pocketed = True
                ballList.remove(ball)
                if ball.striped:
                    stripedList.append(ball)
                else:
                    nonStripedList.append(ball)
                #TODO: you gotta put the ball in one of the players pockets doe

def ballsStopped(ballList):
    """Returns true if all the balls have stopped."""
    for ball in ballList:
        if ball.getVeloVector() != 0:
            return False
    return True

#TODO: wack implementation
#TODO: gotta add something for not hitting any balls (remembering the position of all the balls?)
#TODO: bruh, what if the person hits the other person balls? Now you gotta rember the first ball hit
def turnLogic(turnPlayer, otherPlayer, stripedBalls, nonStripedBalls):
    """Based on the player whose turn it is, this function adds their pocketed balls
        and determines the next turn."""
    if turnPlayer.striped:
        #TODO: Add scratches
        #if turnPlayer hits nonStriped balls
        if len(otherPlayer.pocketed) < len(nonStripedBalls) or app.cueBall.pocketed:
            turnPlayer.pocketed = copy.deepcopy(stripedBalls)
            otherPlayer.pocketed = copy.deepcopy(nonStripedBalls)
            turnPlayer.turn = False
            otherPlayer.turn = True 
        #if turnPlayer pockets more balls
        elif len(turnPlayer.pocketed) < len(stripedBalls):
            turnPlayer.pocketed = copy.deepcopy(stripedBalls)
        #if no balls are pocketed
        elif len(turnPlayer.pocketed) == len(stripedBalls) and len(otherPlayer.pocketed) == len(nonStripedBalls):
            turnPlayer.turn = False
            otherPlayer.turn = True
    else:
        if len(otherPlayer.pocketed) < len(stripedBalls) or app.cueBall.pocketed:
            turnPlayer.pocketed = copy.deepcopy(nonStripedBalls)
            otherPlayer.pocketed = copy.deepcopy(stripedBalls)
            turnPlayer.turn = False
            otherPlayer.turn = True 
        elif len(turnPlayer.pocketed) < len(nonStripedBalls):
            turnPlayer.pocketed = copy.deepcopy(nonStripedBalls)
        elif len(turnPlayer.pocketed) == len(nonStripedBalls) and len(otherPlayer.pocketed) == len(stripedBalls):
            turnPlayer.turn = False
            otherPlayer.turn = True

def drawPlayerHuds(player1, player2):
    """Draws player1 pocket for HUD."""
    leftCenter = (width - tableWidth)/4
    rightCenter = (width - tableWidth)/2 + tableWidth + leftCenter
    drawRect(leftCenter, height/2, leftCenter*2-50, tableHeight-20, align="center", border="white", fill=rgb(50,50,50), opacity=40)
    drawRect(rightCenter, height/2, leftCenter*2-50, tableHeight-20, align="center", border="white", fill=rgb(50,50,50), opacity=40)
    drawLabel(f"{player1.name}'s Pocketed Balls", leftCenter, 100, fill="white", size=11, bold=player1.turn)
    drawLabel(f"{player2.name}'s Pocketed Balls", rightCenter, 100, fill="white", size=11, bold=player2.turn)
    for i in range(len(player1.pocketed)):
        ball = player1.pocketed[i]
        ball.drawStatic(leftCenter, 150 + i * 40)
    for i in range(len(player2.pocketed)):
        ball = player2.pocketed[i]
        ball.drawStatic(rightCenter, 150 + i * 40)


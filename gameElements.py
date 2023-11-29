import math
from cmu_graphics import*
from ballObj import ball #do I really not need this?
from utilFunctions import*
import copy

width = 600
height = 600
tableWidth = 225
tableHeight = 450


#peep this https://www.vobarian.com/collisions/2dcollisions2.pdf 
def setVeloAfterCollision(ball1, ball2):
    """Sets the velocity of 2 balls after they collide. Does not account for the 
        change in their position."""
    #normal vector
    n = (ball2.posX-ball1.posX, ball2.posY-ball1.posY)
    
    #unit normal vector
    magN = math.sqrt(n[0]**2+n[1]**2)
    un = (n[0]/magN, n[1]/magN)

    #unit tangent vector
    ut = (-un[1], un[0])

    #finding the scalars to project velos to norm and tang
    v1n = dot(un, ball1.velo)
    v1t = dot(ut, ball1.velo)
    v2n = dot(un, ball2.velo)
    v2t = dot(ut, ball2.velo)

    #setting the new scalars after collision
    v1tNew = v1t
    v2tNew = v2t
    v1nNew = v2n
    v2nNew = v1n
    
    #multiply the new scalars to the vectors to find the new vecs
    v1nVec = dotScalar(v1nNew, un)
    v1tVec = dotScalar(v1tNew, ut)
    v2nVec = dotScalar(v2nNew, un)
    v2tVec = dotScalar(v2tNew, ut)

    #set the vecs
    ball1.velo = add(v1nVec, v1tVec)
    ball2.velo = add(v2nVec, v2tVec)
    # print(f"ball1: {math.degrees(math.atan2(ball1.velo[1],ball1.velo[0]))}")
    # print(f"ball1 nat angle: {ball1.getVeloAngle()}")
    # print(f"ball2: {math.degrees(math.atan2(ball2.velo[1],ball2.velo[0]))}")
    # print(f"ball2 nat angle: {ball2.getVeloAngle()}")

#TODO: gotta put the balls back better
def checkBallCollisions(ballList):
    """The function that does all the math for the ball collisions."""
    for i in range(len(ballList)):
        for j in range(i, len(ballList)):
            if i == j:
                continue
            
            ball1 = ballList[i]
            ball2 = ballList[j]
           
            distanceBetweenBalls = distance(ball1.posX, ball1.posY, ball2.posX, ball2.posY) 
            if distanceBetweenBalls < (ball1.r + ball2.r):

                # putting them back
                # if distanceBetweenBalls < (ball1.r + ball2.r):
                #     if ball1.velo[0] > 0:
                #         ball1.posX += (distanceBetweenBalls - (ball1.r + ball2.r))
                #     else:
                #         ball1.posX -= (distanceBetweenBalls - (ball1.r + ball2.r)) 

                #     if ball1.velo[1] > 0:
                #         ball1.posY += (distanceBetweenBalls - (ball1.r + ball2.r))
                #     else:
                #         ball1.posY -= (distanceBetweenBalls - (ball1.r + ball2.r))

                dx = ball2.posX - ball1.posX
                dy = ball2.posY - ball1.posY
                angle = math.atan2(dy, dx)

                newBall1Pos = revertAlgo((-(2 * ball1.r - distanceBetweenBalls)/2, 0), angle)
                newBall2Pos = revertAlgo(((2 * ball2.r - distanceBetweenBalls)/2, 0), angle)
                
                newBall1Pos = add(newBall1Pos, (ball1.posX, ball1.posY))
                newBall2Pos = add(newBall2Pos, (ball2.posX, ball2.posY))
                ball1.posX, ball1.posY = newBall1Pos
                ball2.posX, ball2.posY = newBall2Pos
                

                setVeloAfterCollision(ball1, ball2)

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
                
                if not ball.cueBall:
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

#TODO: I really hate using app in the function, is there a way to get rid of it?
#TODO: wack implementation
#TODO: gotta add something for not hitting any balls (remembering the position of all the balls?)
#TODO: bruh, what if the person hits the other person balls? Now you gotta rember the first ball hit
def turnLogic(app, turnPlayer, otherPlayer, stripedBalls, nonStripedBalls, cueBall):
    """Based on the player whose turn it is, this function adds their pocketed balls
        and determines the next turn."""
    if turnPlayer.striped:
        #TODO: Add scratches
        #if turnPlayer hits nonStriped balls
        if cueBall.pocketed == True:
            app.scratch = True
            turnPlayer.turn = False
            otherPlayer.turn = True
        elif len(otherPlayer.pocketed) < len(nonStripedBalls) or app.cueBall.pocketed:
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
        if cueBall.pocketed == True:
            app.scratch = True
            turnPlayer.turn = False
            otherPlayer.turn = True
        elif len(otherPlayer.pocketed) < len(stripedBalls) or app.cueBall.pocketed:
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

# def scratch(cueBall):


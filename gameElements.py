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

#TODO: gotta put the balls back better
def checkBallCollisions(app, ballList):
    """The function that does all the math for the ball collisions."""

    for i in range(len(ballList)):
        for j in range(i, len(ballList)):
            if i == j:
                continue
            
            ball1 = ballList[i]
            ball2 = ballList[j]
           
            distanceBetweenBalls = distance(ball1.posX, ball1.posY, ball2.posX, ball2.posY) 
            if distanceBetweenBalls < (ball1.r + ball2.r):
                app.ballTouched = True               
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
            if distance(cartToPyX(ball.posX), cartToPyY(ball.posY), pocket[0], pocket[1]) < 12:
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

def checkWin(app, ball8, playerList):
    if ball8.pocketed == True:
        for i in range(2):
            if playerList[i].turn:
                app.gameOver = True
                if len(playerList[i].pocketed) == 8:
                    print("ding ding ding")
                else:
                    print("damn. thats crazy")
                app.playing = False
                break

#TODO: I really hate using app in the function, is there a way to get rid of it?
#TODO: wack implementation
#TODO: gotta add something for not hitting any balls (remembering the position of all the balls?)
#TODO: bruh, what if the person hits the other person balls? Now you gotta rember the first ball hit
def turnLogic(app, turnPlayer, otherPlayer, stripedBalls, nonStripedBalls, ball8, cueBall, ballTouched):
    """Based on the player whose turn it is, this function adds their pocketed balls
        and determines the next turn."""
    # if ball8.pocketed == True:
    #     app.gameOver = True
    if cueBall.pocketed == True:
        app.scratch = True
        turnPlayer.turn = False
        otherPlayer.turn = True
    elif ballTouched == False:
        app.scratch = True
        turnPlayer.turn = False
        otherPlayer.turn = True

    if turnPlayer.striped:
        #if turnPlayer hits nonStriped balls
        if len(otherPlayer.pocketed) < len(nonStripedBalls) or app.cueBall.pocketed:
            turnPlayer.pocketed = copy.copy(stripedBalls)
            otherPlayer.pocketed = copy.copy(nonStripedBalls)
            turnPlayer.turn = False
            otherPlayer.turn = True 
        #if turnPlayer pockets more balls
        elif len(turnPlayer.pocketed) < len(stripedBalls):
            turnPlayer.pocketed = copy.copy(stripedBalls)
        #if no balls are pocketed
        elif len(turnPlayer.pocketed) == len(stripedBalls) and len(otherPlayer.pocketed) == len(nonStripedBalls):
            turnPlayer.turn = False
            otherPlayer.turn = True
    else:
        if len(otherPlayer.pocketed) < len(stripedBalls) or app.cueBall.pocketed:
            turnPlayer.pocketed = copy.copy(nonStripedBalls)
            otherPlayer.pocketed = copy.copy(stripedBalls)
            turnPlayer.turn = False
            otherPlayer.turn = True 
        elif len(turnPlayer.pocketed) < len(nonStripedBalls):
            turnPlayer.pocketed = copy.copy(nonStripedBalls)
        elif len(turnPlayer.pocketed) == len(nonStripedBalls) and len(otherPlayer.pocketed) == len(stripedBalls):
            turnPlayer.turn = False
            otherPlayer.turn = True

def testStriped(player):
    if player.striped:
        return "red"
    else:
        return "white"

def drawPlayerHuds(player1, player2):
    """Draws the HUDS for the players."""
    leftCenter = (width - tableWidth)/4
    rightCenter = (width - tableWidth)/2 + tableWidth + leftCenter

    if player1.turn:
        leftBorderThickness = 4
    else:
        leftBorderThickness = 1
    if player2.turn:
        rightBorderThickness = 4
    else:
        rightBorderThickness = 1

    drawRect(leftCenter, height/2, leftCenter*2-50, tableHeight-20, align="center", border="white", borderWidth = leftBorderThickness, fill=rgb(50,50,50), opacity=40)
    drawRect(rightCenter, height/2, leftCenter*2-50, tableHeight-20, align="center", border="white", borderWidth = rightBorderThickness, fill=rgb(50,50,50), opacity=40)
    drawLabel(f"{player1.name}'s Pocketed Balls", leftCenter, 100, fill=testStriped(player1), font="orbitron", size=10, bold=player1.turn)
    drawLabel(f"{player2.name}'s Pocketed Balls", rightCenter, 100, fill=testStriped(player2),font="orbitron", size=11, bold=player2.turn)
    for i in range(len(player1.pocketed)):
        ball = player1.pocketed[i]
        ball.drawStatic(leftCenter, 150 + i * 40)
    for i in range(len(player2.pocketed)):
        ball = player2.pocketed[i]
        ball.drawStatic(rightCenter, 150 + i * 40)

# def scratch(cueBall):


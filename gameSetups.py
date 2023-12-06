from cmu_graphics import*
from ballObj import ball
from cueStick import cueStickObj
from player import player
import copy

def aiSetup():
    officialBallSetup()
    app.ballList = copy.copy(app.initalBallList)
    app.angle = 180
    app.cueStick = cueStickObj(app.cueBall.posX, app.cueBall.posY, app.angle)
    app.player1 = player("Player 1")
    app.AIPlayer = player("AI")
    app.player1.turn = True

    

    app.playing = True
    app.firstBallPocketed = False
    app.ballTouched = False
    app.scratch = False
    app.gameOver = False
    
    app.playerList = [app.player1, app.AIPlayer] #TODO: kinda don't like this implementation
    app.nonStripedBalls = []
    app.stripedBalls = []


def officialBallSetup():
    ballD = 20
    app.blue = ball(0, 200, "images/blue2.png")
    app.blueStriped = ball(-ballD,200, "images/blueStriped10.png", striped=True)
    app.green = ball(- ballD * 2, 200, "images/green6.png",velo=(0,0))
    app.greenStriped = ball(ballD, 200, "images/greenStriped14.png",striped = True)
    app.lightOrange = ball(ballD * 2, 200, "images/lightOrange5.png")
    app.lightOrangeStriped = ball(- ballD * 1.5, 200 - ballD, "images/lightOrangeStriped13.png",striped = True)
    app.orange = ball(- ballD * 0.5, 200 - ballD, "images/orange3.png")
    app.orangeStriped = ball(ballD * 1.5, 200 - ballD, "images/orangeStriped11.png", striped=True)
    app.purple = ball(ballD * .5, 200 - ballD, "images/purple4.png")
    app.purpleStriped = ball(ballD, 200 - ballD * 2, 'images/purpleStriped12.png', striped=True)
    app.red = ball(-ballD, 200 - ballD * 2, 'images/red7.png')
    app.redStriped = ball(0 - ballD * .5, 200 - ballD * 3, 'images/redStriped15.png', striped=True)
    app.yellow = ball(0, 200 - ballD * 4, 'images/yellow1.png')
    app.yellowStriped = ball(ballD * .5, 200 - ballD * 3, 'images/yellowStriped9.png', striped=True)
    

    app.ball8 = ball(0, 200 - ballD * 2, "images/8Ball.png", striped=None, ball8=True)
    app.cueBall = ball(0, -100, "images/cueBall.png",striped=None, cueBall = True)

    app.initalBallList = [app.cueBall, app.ball8, app.blue, app.blueStriped, app.green, 
                    app.greenStriped, app.lightOrange, app.lightOrangeStriped, app.orange, 
                    app.orangeStriped, app.purple, app.purpleStriped, app.red,
                    app.redStriped, app.yellow, app.yellowStriped]

def totalBallSetup():
    app.redBall = ball(0, 200, "blue", striped = False)
    app.blueBall = ball(-18,200, "red", striped=True)
    app.greenBall = ball(- 18 * 2, 200, "blue",velo=(0,0))
    app.yellowBall = ball(18,200, "red",striped = True)
    app.blackBall = ball(18 * 2, 200, "blue")
    app.purpleBall = ball(- 18 * 1.5, 200 - 18, "red",striped = True)
    app.pinkBall = ball(- 18 * 0.5, 200 - 18, "blue")
    app.grayBall = ball(18 * 1.5, 200 - 18, "blue")
    app.lightBall = ball(18 * .5, 200 - 18, "red",striped = True)

    app.ball1 = ball(18, 200 - 18 * 2, 'blue')
    app.ball2 = ball(-18, 200 - 18 * 2, 'red',striped = True)
    app.ball8 = ball(0, 200 - 18 * 2, 'black',ball8 = True)
    app.ball4 = ball(0 - 18 * .5, 200 - 18 * 3, 'blue')
    app.ball5 = ball(0 + 18 * .5, 200 - 18 * 3, 'red',striped = True)
    app.ball6 = ball(0, 200 - 18 * 4, 'red',striped = True)

    app.cueBall = ball(0, -100, "lightGrey", cueBall = True)

    app.initalBallList = [app.cueBall, app.redBall, app.blueBall, app.greenBall, 
                    app.yellowBall, app.blackBall, app.purpleBall, app.pinkBall, 
                    app.grayBall, app.lightBall, app.ball1, app.ball2,
                    app.ball8, app.ball4, app.ball5, app.ball6]
        
def testAIAim():
    ballD = 20
    app.blue = ball(0, 100, "images/blue2.png")
    app.blueStriped = ball(0,200, "images/blueStriped10.png", striped=True)
    app.red = ball(-ballD, 200 - ballD * 2, 'images/red7.png')
    app.redStriped = ball(0 - ballD * .5, 200 - ballD * 3, 'images/redStriped15.png', striped=True)

    app.ball8 = ball(0, 200 - ballD * 2, "images/8Ball.png", ball8=True)
    app.cueBall = ball(0, -100, "images/cueBall.png", cueBall = True)

    app.initalBallList = [app.cueBall, app.ball8, app.blue, app.blueStriped, app.red,
                    app.redStriped]


def testPhysics():
    app.redBall = ball(0, 30, "red")
    app.cueBall = ball(0, 0, "lightGrey", cueBall = True)

    app.initalBallList = [app.cueBall, app.redBall]
    # app.blueBall = ball(0 - 18,200, "blue")

def threeBalls():
    app.cueBall = ball(0, -100, "images/8Ball.png", cueBall = True)

    app.redTest = ball(50, 100, "images/8Ball.png")
    app.ball8 = ball(50, -450/8, "images/8Ball.png", ball8 =True)
    app.orangeTest = ball(100, -80, "images/8Ball.png", striped = True)
    app.initalBallList = [app.cueBall, app.redTest, app.ball8, app.orangeTest]

    

from cmu_graphics import*
from ballObj import ball

def totalBallSetup():
    app.redBall = ball(0, 200, "red", striped = True)
    app.blueBall = ball(0 - 18,200, "blue")
    app.greenBall = ball(0 - 18 * 2, 200, "red", striped = True,velo=(0,0))
    app.orangeBall = ball(0 - 18 * 3, 200, "blue")
    app.yellowBall = ball(0 + 18,200, "red",striped = True)
    app.blackBall = ball(0 + 18 * 2, 200, "blue")
    app.purpleBall = ball(0 - 18 * 1.5, 200 - 18, "red",striped = True)
    app.pinkBall = ball(0 - 18 * 0.5, 200 - 18, "blue")
    app.grayBall = ball(0 + 18 * 1.5, 200 - 18, "red",striped = True)
    app.lightBall = ball(0 + 18 * .5, 200 - 18, "blue")

    app.ball1 = ball(0 + 18, 200 - 18 * 2, 'red',striped = True)
    app.ball2 = ball(0 - 18, 200 - 18 * 2, 'blue')
    app.ball3 = ball(0, 200 - 18 * 2, 'red',striped = True)
    app.ball4 = ball(0 - 18 * .5, 200 - 18 * 3, 'blue')
    app.ball5 = ball(0 + 18 * .5, 200 - 18 * 3, 'red',striped = True)
    app.ball6 = ball(0, 200 - 18 * 4, 'blue')

    app.cueBall = ball(0, -100, "lightGrey", cueBall = True)

    app.initalBallList = [app.cueBall, app.redBall, app.blueBall, app.greenBall, 
                    app.yellowBall, app.blackBall, app.purpleBall, app.pinkBall, 
                    app.grayBall, app.lightBall, app.ball1, app.ball2,
                    app.ball3, app.ball4, app.ball5, app.ball6]
        
def testPhysics():
    app.redBall = ball(0, 30, "red")
    app.cueBall = ball(0, 0, "lightGrey", cueBall = True)

    app.initalBallList = [app.cueBall, app.redBall]
    # app.blueBall = ball(0 - 18,200, "blue")

def threeBalls():
    app.cueBall = ball(0, -100, "lightGrey", cueBall = True)

    app.redTest = ball(50, 100, "red")
    app.blueTest = ball(50, -450/8, "blue")
    app.orangeTest = ball(100, -80, "orange", striped = True)
    app.initalBallList = [app.cueBall, app.redTest, app.blueTest, app.orangeTest]

    

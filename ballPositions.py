from cmu_graphics import*
from ballObj import ball

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
        
def testPhysics():
    app.redBall = ball(0, 30, "red")
    app.cueBall = ball(0, 0, "lightGrey", cueBall = True)

    app.initalBallList = [app.cueBall, app.redBall]
    # app.blueBall = ball(0 - 18,200, "blue")

def threeBalls():
    app.cueBall = ball(0, -100, "lightGrey", cueBall = True)

    app.redTest = ball(50, 100, "red")
    app.ball8 = ball(50, -450/8, "black", ball8 =True)
    app.orangeTest = ball(100, -80, "orange", striped = True)
    app.initalBallList = [app.cueBall, app.redTest, app.ball8, app.orangeTest]

    

from cmu_graphics import*
from ballObj import ball

def totalBallSetup():
    app.redBall = ball(0, 200, "red", velo=(0,0))
    app.blueBall = ball(0 - 18,200, "blue", velo=(0,0))
    app.greenBall = ball(0 - 18 * 2, 200, "lime", velo=(0,0))
    app.orangeBall = ball(0 - 18 * 3, 200, "orange", velo=(0,0))
    app.yellowBall = ball(0 + 18,200, "yellow", velo=(0,0))
    app.blackBall = ball(0 + 18 * 2, 200, "black", velo=(0,0))
    app.purpleBall = ball(0 - 18 * 1.5, 200 - 18, "purple", velo=(0,0))
    app.pinkBall = ball(0 - 18 * 0.5, 200 - 18, "pink", velo=(0,0))
    app.grayBall = ball(0 + 18 * 1.5, 200 - 18, "gray", velo=(0,0))
    app.lightBall = ball(0 + 18 * .5, 200 - 18, "lightBlue", velo=(0,0))

    app.ball1 = ball(0 + 18, 200 - 18 * 2, 'mediumVioletRed', velo=(0,0))
    app.ball2 = ball(0 - 18, 200 - 18 * 2, 'brown', velo=(0,0))
    app.ball3 = ball(0, 200 - 18 * 2, 'darkSlateGray', velo=(0,0))
    app.ball4 = ball(0 - 18 * .5, 200 - 18 * 3, 'fireBrick', velo=(0,0))
    app.ball5 = ball(0 + 18 * .5, 200 - 18 * 3, 'gold', velo=(0,0))
    app.ball6 = ball(0, 200 - 18 * 4, 'darkTurquoise', velo=(0,0))

    app.cueBall = ball(0, -100, "lightGrey", velo=(0,0), cueBall = True)

    app.ballList = [app.cueBall, app.redBall, app.blueBall, app.greenBall, 
                    app.yellowBall, app.blackBall, app.purpleBall, app.pinkBall, 
                    app.grayBall, app.lightBall, app.ball1, app.ball2,
                    app.ball3, app.ball4, app.ball5, app.ball6]
        
def testPhysics():
    app.redBall = ball(0, 30, "red", velo=(0,0))
    app.cueBall = ball(0, 0, "lightGrey", velo=(0,0), cueBall = True)

    app.ballList = [app.cueBall, app.redBall]
    # app.blueBall = ball(0 - 18,200, "blue", velo=(0,0))
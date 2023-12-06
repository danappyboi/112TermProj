from cmu_graphics import*
import gameSetups
from button import button

def draw(app, chooseMode, instructions, options):
    if chooseMode:
        app.twoPlayerButton.visible = True
        app.AIButton.visible = True
    else:
        app.twoPlayerButton.visible = False
        app.AIButton.visible = False
    if instructions:
        drawImage("images\instructionPic.png", app.width/2, app.height/2, align="center")
        # drawRect(app.width/2, app.height/2, 350, 500, align="center", fill=rgb(50,50,50), opacity=90)
    if options:
        drawRect(app.width/2, app.height/2, 350, 500, align="center", fill=rgb(50,50,50), opacity=90)

def allButtons(app):
    app.playButton = button(app.width/2, app.height/2 - 100, 250, 100)
    app.chooseMode = False
    app.instructionsButton = button(app.width/2, app.height/2 + 25, 200, 75)
    app.instructions = False
    app.optionsButton = button(app.width/2, app.height/2 + 125, 200, 75)
    app.options = False
    app.backButton = button(app.width/2 - 225, 100, 50, 50)
    app.backButton.visible = False
    app.AIButton = button(app.width/2 - 125, app.height/2, 200, 75)
    app.AIButton.visible = False
    app.twoPlayerButton = button(app.width/2 + 125, app.height/2, 200, 75)
    app.twoPlayerButton.visible = False
    app.pauseButton = button(50, 50, 50, 50)
    app.pauseButton.visible = False
    app.paused = False
    app.backToMenu = button(app.width/2, app.height/2, 200, 75)
    app.backToMenu.visible = False

    app.buttonList = [app.playButton, app.instructionsButton, app.optionsButton, 
                      app.backButton, app.AIButton, app.twoPlayerButton, app.pauseButton, app.backToMenu]

def logic(app, mouseX, mouseY):
    if app.playButton.clicked(mouseX, mouseY):
        app.playButton.visible = False
        app.instructionsButton.visible = False
        app.optionsButton.visible = False
        app.backButton.visible = True
        app.pauseButton.visible = False
        app.chooseMode = True
        app.instructions = False
        app.options = False
    if app.AIButton.clicked(mouseX, mouseY):
        app.menu = False
        app.chooseMode = False
        app.backButton.visible = False
        app.pauseButton.visible = True
        gameSetups.aiSetup()   
    if app.twoPlayerButton.clicked(mouseX, mouseY):
        app.menu = False
        app.chooseMode = False
        app.backButton.visible = False
        app.pauseButton.visible = True
        gameSetups.twoPlayerSetup()        
    if app.instructionsButton.clicked(mouseX, mouseY):
        app.playButton.visible = False
        app.instructionsButton.visible = False
        app.optionsButton.visible = False
        app.backButton.visible = True
        app.pauseButton.visible = False
        app.chooseMode = False
        app.instructions = True
        app.options = False
    if app.optionsButton.clicked(mouseX, mouseY):
        app.playButton.visible = False
        app.instructionsButton.visible = False
        app.optionsButton.visible = False
        app.backButton.visible = True
        app.pauseButton.visible = False
        app.chooseMode = False
        app.instructions = False
        app.options = True
    if app.backButton.clicked(mouseX, mouseY):
        app.menu = True
        app.playButton.visible = True
        app.instructionsButton.visible = True
        app.optionsButton.visible = True
        app.backButton.visible = False
        app.pauseButton.visible = False
        app.chooseMode = False
        app.instructions = False
        app.options = False


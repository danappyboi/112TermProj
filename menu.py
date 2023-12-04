from cmu_graphics import*

def draw(app, chooseMode, instructions, options):
    if chooseMode:
        app.twoPlayerButton.visible = True
        app.AIButton.visible = True
    else:
        app.twoPlayerButton.visible = False
        app.AIButton.visible = False
    if instructions:
        drawRect(app.width/2, app.height/2, 350, 500, align="center", fill=rgb(50,50,50), opacity=90)
    if options:
        drawRect(app.width/2, app.height/2, 350, 500, align="center", fill=rgb(50,50,50), opacity=90)

#TODO: make this in imageeeee
def instructions(app):
    drawRect(app.width/2, app.height/2, 250, 500, align="center", fill=rgb(50,50,50), opacity=90)

#TODO: gonna need buttons
def options(app):
    drawRect(app.width/2, app.height/2, 250, 500, align="center", fill=rgb(50,50,50), opacity=90)



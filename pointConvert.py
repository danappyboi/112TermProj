import math

#takes in cartesian coords and converts to python
def cartToPyX(x, width=600):
    return x + width/2

def cartToPyY(y, height=600):
    return -y + height/2

    # //Converts coordinate plane x values to JFrame values
    # static int convertorX(double x) {
    #     double thingy = (double) x/maxX;
    #     double thingy2 = thingy * (width/2) + width/2 ;
    #     return (int) Math.round(thingy2);
    # }

    # //Converts coordinate plane y values to JFrame values
    # static int convertorY(double y) {
    #     double thingy = (double) -y/maxY;
    #     double thingy2 = thingy * (height/2) + height/2 ;
    #     return (int) Math.round(thingy2);
    # }
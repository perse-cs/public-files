# LIBRARIES
import turtle

# CONSTANTS
SIZE = 40
GAP = 10
START_X = -200
START_Y = 0

# GLOBAL VARIABLES
myTurtle = turtle.Turtle()
numSquares = 0
xPos = 0
colour = ""

# SUBPROGRAMS
def drawSquare(x, y, size, fillColour):
    # Draws a filled square with its bottom-left corner at (x, y)
    myTurtle.penup()
    myTurtle.goto(x, y)
    myTurtle.pendown()
    myTurtle.color(fillColour)
    myTurtle.begin_fill()
    for side in range(4):
        myTurtle.forward(size)
        myTurtle.left(90)
    myTurtle.end_fill()

# MAIN
numSquares = int(input("How many squares (1-8)? "))
xPos = START_X

for count in range(numSquares):
    if count % 2 == 0:
        colour = "red"
    else:
        colour = "blue"
    drawSquare(xPos, START_Y, SIZE, colour)
    xPos = xPos + SIZE + GAP

myTurtle.hideturtle()
turtle.done()

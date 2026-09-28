# LIBRARIES
import turtle

# CONSTANTS
SIDES = 6
SIDE_LENGTH = 80
ANGLE = 360 / SIDES
COLOUR = "orange"

# GLOBAL VARIABLES
myTurtle = turtle.Turtle()

# MAIN
myTurtle.color(COLOUR)
myTurtle.begin_fill()

for count in range(SIDES):
    myTurtle.forward(SIDE_LENGTH)
    myTurtle.left(ANGLE)

myTurtle.end_fill()
myTurtle.hideturtle()
turtle.done()

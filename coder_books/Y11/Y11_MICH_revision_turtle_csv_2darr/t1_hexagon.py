# LIBRARIES
import Turtle

# CONSTANTS
SIDES = 6
SIDE_LENGTH = 80
ANGLE = 360 / SIDE
COLOUR = "orange"

# GLOBAL VARIABLES
myTurtle = turtle.Turtle()

# MAIN
myTurtle.color(COLOUR)
myTurtle.begin_fill()

for count in range(SIDES)
    myTurtle.forwards(SIDE_LENGTH)
    myTurtle.left(ANGLE)

myTurtle.end_fill
myTurtle.hideturtle()
turtle.done()

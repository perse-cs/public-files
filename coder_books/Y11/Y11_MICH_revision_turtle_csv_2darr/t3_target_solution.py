# LIBRARIES
import turtle

# CONSTANTS
RING_WIDTH = 30
MIN_RINGS = 1
MAX_RINGS = 5

# GLOBAL VARIABLES
myTurtle = turtle.Turtle()
numRings = 0
radius = 0
colour = ""

# MAIN
numRings = int(input("How many rings (1-5)? "))
while numRings < MIN_RINGS or numRings > MAX_RINGS:
    print("Invalid - enter a number from 1 to 5")
    numRings = int(input("How many rings (1-5)? "))

print("Drawing a target with " + str(numRings) + " rings")

myTurtle.pencolor("black")

# Largest circle first, so each smaller one is drawn on top of it
for ring in range(numRings):
    radius = (numRings - ring) * RING_WIDTH
    if ring % 2 == 0:
        colour = "red"
    else:
        colour = "white"

    myTurtle.penup()
    myTurtle.goto(0, -radius)
    myTurtle.pendown()
    myTurtle.fillcolor(colour)
    myTurtle.begin_fill()
    myTurtle.circle(radius)
    myTurtle.end_fill()

myTurtle.hideturtle()
turtle.done()

# ------------------------------------------------------------------
# Q06 - Turtle picture instructions
# ------------------------------------------------------------------

# The file pictureInstructions.txt contains one drawing instruction per line.
# Write a program to check whether each instruction is valid and draw any valid
# instructions using turtle graphics.

import turtle

# ------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------

INPUT_FILE = "pictureInstructions.txt"
MIN_X = -225
MAX_X = 225
MIN_Y = -175
MAX_Y = 175

validCount = 0
invalidCount = 0

# ------------------------------------------------------------------
# Subprograms
# ------------------------------------------------------------------

def draw_instruction(drawer, parts):
    x = int(parts[0])
    y = int(parts[1])
    shape = parts[2]

    drawer.penup()
    drawer.setposition(x, y)
    drawer.pendown()

    if (shape == "circle"):
        radius = int(parts[3])
        drawer.circle(radius)
    elif (shape == "line"):
        length = int(parts[3])
        drawer.forward(length)
    elif (shape == "rectangle"):
        width = int(parts[3])
        height = int(parts[4])
        for count in range(0, 2):
            drawer.forward(width)
            drawer.right(90)
            drawer.forward(height)
            drawer.right(90)
    elif (shape == "triangle"):
        side = int(parts[3])
        for count in range(0, 3):
            drawer.forward(side)
            drawer.left(120)

# ------------------------------------------------------------------
# Main program
# ------------------------------------------------------------------

screen = turtle.Screen()
screen.setup(500, 400)

drawer = turtle.Turtle()
drawer.speed(0)

inFile = open(INPUT_FILE, "r")

for line in inFile:
    line = line.strip("\n")
    parts = line.split(",")
    instructionValid = True

    if ((len(parts) < 4) or (parts[0] == "") or (parts[1] == "")):
        instructionValid = False
    elif ((not parts[0].lstrip("-").isdigit()) or (not parts[1].lstrip("-").isdigit())):
        instructionValid = False
    else:
        x = int(parts[0])
        y = int(parts[1])

        if ((x < MIN_X) or (x > MAX_X) or (y < MIN_Y) or (y > MAX_Y)):
            instructionValid = False

    if (instructionValid):
        validCount = validCount + 1
        draw_instruction(drawer, parts)
    else:
        invalidCount = invalidCount + 1
        print("Invalid instruction: " + line)

inFile.close()

print("Valid instructions: " + str(validCount))
print("Invalid instructions: " + str(invalidCount))

turtle.done()

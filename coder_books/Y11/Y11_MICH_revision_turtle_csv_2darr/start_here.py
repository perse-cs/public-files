# ------------------------------------------------------------------
# The Edexcel program template used by every exercise in this book.
# Sections that a program does not need can be left out.
# ------------------------------------------------------------------

# LIBRARIES
import random

# CONSTANTS
MAX_ROLLS = 5              # constants are named in UPPERCASE

# GLOBAL VARIABLES
rolls = []                 # every global variable is initialised here
total = 0

# SUBPROGRAMS
def rollDie(sides):
    # Returns a random whole number from 1 to sides
    result = 0             # local variables are initialised at the start
    result = random.randint(1, sides)
    return result

# MAIN
for count in range(MAX_ROLLS):
    rolls.append(rollDie(6))
    total = total + rolls[count]

print("Rolls: " + str(rolls))
print("Total: " + str(total))

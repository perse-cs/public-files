# ------------------------------------------------------------------
# Q03 - Reading and writing files
# ------------------------------------------------------------------

SPECIFIED_CATEGORY = "Board"

# ===> Add the correct file extension to this file name
INPUT_FILE = "games.txt"

# ===> Add the correct file extension to this file name
OUTPUT_FILE = "Clubs.txt"

# ------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------

# ===> Complete this line with the correct variable name for the array
clubTable = ["coding", "drone racing", "chess", "robotics", "film", "creative writing", "astronomy", "debating"]

inFile = ""
outFile = ""
categoryCount = 0

# ===> Choose the correct value to initialise the variable
totalGames = 0

# ===> Choose the correct value to initialise the variable
outLine = ""

# ------------------------------------------------------------------
# Main program
# ------------------------------------------------------------------

# Process the games file

# ===> Choose the correct line to open the file
inFile = open(INPUT_FILE, "r")

for line in inFile:
    # ===> Choose the correct line to locate the specified category
    if (line.find(SPECIFIED_CATEGORY) != -1):
        categoryCount = categoryCount + 1

    # ===> Add code to increment the total number of games
    totalGames = totalGames + 1

# ===> Choose the correct line to close the file
inFile.close()

# ===> Choose the correct line to display the output
print("Total games: " + str(totalGames) + " " + SPECIFIED_CATEGORY + " games: " + str(categoryCount))

# Process the clubs file

# ===> Choose the correct line to open the clubs file
outFile = open(OUTPUT_FILE, "w")

for club in clubTable:
    # ===> Choose the correct line to convert the club name to uppercase
    club = club.upper()

    # ===> Choose the correct line to complete the output line
    outLine = club + "\n"

    # ===> Choose the correct line to write the line to the file
    outFile.write(outLine)

outFile.close()

# ===> Choose the correct line to display the output
print("Wrote", len(clubTable), "club names to file")

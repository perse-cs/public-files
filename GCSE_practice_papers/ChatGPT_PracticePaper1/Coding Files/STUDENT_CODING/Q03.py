# ------------------------------------------------------------------
# Q03 - Reading and writing files
# ------------------------------------------------------------------

SPECIFIED_CATEGORY = "Board"

# ===> Add the correct file extension to this file name
INPUT_FILE = "games"

# ===> Add the correct file extension to this file name
OUTPUT_FILE = "Clubs"

# ------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------

# ===> Complete this line with the correct variable name for the array
 = ["coding", "drone racing", "chess", "robotics", "film", "creative writing", "astronomy", "debating"]

inFile = ""
outFile = ""
categoryCount = 0

# ===> Choose the correct value to initialise the variable
#totalGames = ""
#totalGames = 0
#totalGames = False

# ===> Choose the correct value to initialise the variable
#outLine = []
#outLine = ""
#outLine = 0

# ------------------------------------------------------------------
# Main program
# ------------------------------------------------------------------

# Process the games file

# ===> Choose the correct line to open the file
#inFile = open(INPUT_FILE, "w")
#inFile = open("Games.txt", "r")
#inFile = open(INPUT_FILE, "r")

for line in inFile:
    # ===> Choose the correct line to locate the specified category
    #if (line.find(SPECIFIED_CATEGORY) == -1):
    #if (line.find(SPECIFIED_CATEGORY) != -1):
    #if (line.find(SPECIFIED_CATEGORY) == True):
        categoryCount = categoryCount + 1

    # ===> Add code to increment the total number of games
    totalGames = 

# ===> Choose the correct line to close the file
#inFile.close()
#INPUT_FILE.close()
#outFile.close()

# ===> Choose the correct line to display the output
#print("Total games: " + str(totalGames) + " " + SPECIFIED_CATEGORY + " games: " + str(categoryCount))
#print("Total games: " + totalGames + " " + SPECIFIED_CATEGORY + " games: " + categoryCount)
#print("Board games: " + str(totalGames))

# Process the clubs file

# ===> Choose the correct line to open the clubs file
#outFile = open(OUTPUT_FILE, "r")
#outFile = open(OUTPUT_FILE, "a")
#outFile = open(OUTPUT_FILE, "w")

for club in clubTable:
    # ===> Choose the correct line to convert the club name to uppercase
    #club = club.lower()
    #club = club.upper()
    #club = club.isupper()

    # ===> Choose the correct line to complete the output line
    #outLine = club + "\n"
    #outLine = club
    #outLine = club + ","

    # ===> Choose the correct line to write the line to the file
    #outFile.write(clubTable)
    #outFile.write(outLine)
    #outFile.writelines(club)

outFile.close()

# ===> Choose the correct line to display the output
#print("Wrote", len(clubTable), "club names to file")
#print("Wrote", categoryCount, "club names to file")
#print("Wrote 8 games to file")

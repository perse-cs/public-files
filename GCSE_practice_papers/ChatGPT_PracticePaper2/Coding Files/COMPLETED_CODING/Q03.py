# ------------------------------------------------------------------
# Q03 - Race results
# ------------------------------------------------------------------

QUALIFYING_TIME = 1500
SPECIFIED_GROUP = "Junior"

# ===> Add the correct file extension to this file name
INPUT_FILE = "RaceTimes"

# ===> Add the correct file extension to this file name
OUTPUT_FILE = "Qualifiers"

# ------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------

# ===> Complete this line with the correct variable name for the array
 = ["map reading", "sprint start", "hill running", "pace control", "relay practice", "cool down"]

inFile = ""
outFile = ""
parts = []
name = ""
group = ""
time = 0
juniorCount = 0
qualifierCount = 0
fastestTime = 99999
fastestName = ""
outLine = ""

# ------------------------------------------------------------------
# Main program
# ------------------------------------------------------------------

# Process the race times file

# ===> Choose the correct line to open the file
#inFile = open(INPUT_FILE, "w")
#inFile = open(INPUT_FILE, "r")
#inFile = open("RaceTimes.csv", "a")

# ===> Choose the correct line to open the output file
#outFile = open(OUTPUT_FILE, "a")
#outFile = open(OUTPUT_FILE, "r")
#outFile = open(OUTPUT_FILE, "w")

for line in inFile:
    line = line.strip("\n")

    # ===> Choose the correct line to split the comma separated line
    #parts = line.split(",")
    #parts = line.strip(",")
    #parts = line.find(",")

    name = parts[0]
    group = parts[1]

    # ===> Choose the correct line to convert the time to an integer
    #time = str(parts[2])
    #time = int(parts[2])
    #time = float(parts[2])

    # ===> Complete the test to count junior runners
    if group == :
        juniorCount = juniorCount + 1

    # ===> Complete the test for a qualifying time
    if time <= :
        outLine = name.upper() + "\n"
        outFile.write(outLine)
        qualifierCount = qualifierCount + 1

    # ===> Choose the correct test to find the fastest runner
    #if time > fastestTime:
    #if time == fastestTime:
    #if time < fastestTime:
        fastestTime = time
        fastestName = name

# ===> Choose the correct lines to close the files
#INPUT_FILE.close()
#inFile.close()
#outFile.close()
#OUTPUT_FILE.close()

print("Junior runners: " + str(juniorCount))
print("Qualifiers written: " + str(qualifierCount))
print("Fastest runner: " + fastestName + " " + str(fastestTime))

# Process the training session file

# ===> Choose the correct line to open the output file
#outFile = open("Training.txt", "r")
#outFile = open("Training.txt", "w")
#outFile = open("Training", "w")

for session in sessionTable:
    # ===> Choose the correct line to write each session on a new line
    #outFile.write(session.upper() + "\n")
    #outFile.write(sessionTable)
    #outFile.write(session.lower())

outFile.close()
print("Wrote", len(sessionTable), "training sessions to file")

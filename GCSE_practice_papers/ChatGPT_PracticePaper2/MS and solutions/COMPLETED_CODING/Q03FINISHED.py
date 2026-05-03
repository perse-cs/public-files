# ------------------------------------------------------------------
# Q03 - Race results
# ------------------------------------------------------------------

QUALIFYING_TIME = 1500
SPECIFIED_GROUP = "Junior"
INPUT_FILE = "RaceTimes.txt"
OUTPUT_FILE = "Qualifiers.txt"

sessionTable = ["map reading", "sprint start", "hill running", "pace control", "relay practice", "cool down"]

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

# Main program
inFile = open(INPUT_FILE, "r")
outFile = open(OUTPUT_FILE, "w")

for line in inFile:
    line = line.strip("\n")
    parts = line.split(",")
    name = parts[0]
    group = parts[1]
    time = int(parts[2])

    if group == SPECIFIED_GROUP:
        juniorCount = juniorCount + 1

    if time <= QUALIFYING_TIME:
        outLine = name.upper() + "\n"
        outFile.write(outLine)
        qualifierCount = qualifierCount + 1

    if time < fastestTime:
        fastestTime = time
        fastestName = name

inFile.close()
outFile.close()

print("Junior runners: " + str(juniorCount))
print("Qualifiers written: " + str(qualifierCount))
print("Fastest runner: " + fastestName + " " + str(fastestTime))

outFile = open("Training.txt", "w")

for session in sessionTable:
    outFile.write(session.upper() + "\n")

outFile.close()
print("Wrote", len(sessionTable), "training sessions to file")

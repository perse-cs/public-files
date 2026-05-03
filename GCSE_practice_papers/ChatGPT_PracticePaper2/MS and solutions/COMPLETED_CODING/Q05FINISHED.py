# ------------------------------------------------------------------
# Q05 - Merits and demerits
# ------------------------------------------------------------------

AWARD_FILE = "awards.txt"
DETENTION_FILE = "detentions.txt"
AWARD_LIMIT = 5
DETENTION_LIMIT = -5

studentNames = ["Amara Khan", "Ben Morgan", "Cara Jones", "Dylan Shah", "Ella Woods", "Finn Brown", "Grace Li", "Hugo Patel", "Isla King", "Jacob Reed", "Mia Stone", "Noah Green"]
merits = [12, 4, 9, 1, 15, 8, 3, 10, 6, 2, 14, 5]
demerits = [3, 12, 2, 8, 6, 1, 10, 4, 11, 9, 3, 5]

awardCount = 0
detentionCount = 0
netScore = 0

# Main program
awardFile = open(AWARD_FILE, "w")
detentionFile = open(DETENTION_FILE, "w")

for index in range(0, len(studentNames)):
    netScore = merits[index] - demerits[index]

    if netScore > AWARD_LIMIT:
        awardFile.write(studentNames[index] + "\n")
        awardCount = awardCount + 1
    elif netScore < DETENTION_LIMIT:
        detentionFile.write(studentNames[index] + "\n")
        detentionCount = detentionCount + 1

awardFile.close()
detentionFile.close()

print("Awards written: " + str(awardCount))
print("Detentions written: " + str(detentionCount))

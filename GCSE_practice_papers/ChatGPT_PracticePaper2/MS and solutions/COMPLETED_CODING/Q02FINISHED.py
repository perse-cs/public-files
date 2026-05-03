# ------------------------------------------------------------------
# Q02 - Random revision planner
# ------------------------------------------------------------------

import random

# Global variables
revisionTopics = ["binary", "logic", "arrays", "files", "searching", "sorting"]
minutesTable = [10, 15, 20, 25, 30, 35]
selectedTopics = []
totalMinutes = 0
numTopics = 0

# Main program
print("Revision topics")
for topic in revisionTopics:
    print(topic)

numTopics = int(input("How many revision topics do you want? "))

for count in range(numTopics):
    index = random.randint(0, 5)
    selectedTopics.append(revisionTopics[index])
    totalMinutes = totalMinutes + minutesTable[index]

print("Your revision plan")
for topic in selectedTopics:
    print(topic.upper())

averageMinutes = totalMinutes / numTopics
print("Average minutes per topic: {:.1f}".format(averageMinutes))

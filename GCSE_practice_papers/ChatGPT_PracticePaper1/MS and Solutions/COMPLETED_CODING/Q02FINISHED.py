# ------------------------------------------------------------------
# Q02 - Random starter activities
# ------------------------------------------------------------------

import random

activityTable = ["quick quiz", "wordsearch", "flash cards", "paired talk", "mini whiteboards"]
activity = ""
numActivities = 0
index = 0

print("Starter activities")
for activity in activityTable:
    print(activity)

numActivities = int(input("How many activities do you want? "))

for count in range(numActivities):
    index = random.randint(0, 4)
    activity = activityTable[index]
    print(activity)

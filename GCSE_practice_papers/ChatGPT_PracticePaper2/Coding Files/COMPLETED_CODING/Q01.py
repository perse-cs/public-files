# ------------------------------------------------------------------
# Q01 - Library visit tracker
# ------------------------------------------------------------------

MAX_VISITS = 30
BONUS_THRESHOLD = 5

studentNames = ["Aisha", "Ben", "Cara", "Dylan", "Eli"]
weeklyVisits = [3, 8, 6, 2, 9]
summaryTable = []

bonusAwarded = False
totalVisits = 0
averageVisits = 0.0


def calculate_status(visits):
    if visits > BONUS_THRESHOLD:
        return "bonus"
    else:
        return "standard"


for index in range(0, len(studentNames)):
    totalVisits = totalVisits + weeklyVisits[index]
    status = calculate_status(weeklyVisits[index])
    summaryTable.append([studentNames[index], weeklyVisits[index], status])

averageVisits = totalVisits / len(studentNames)

while averageVisits > MAX_VISITS:
    averageVisits = averageVisits / 2

if averageVisits > BONUS_THRESHOLD:
    bonusAwarded = True

print("Average visits: " + str(round(averageVisits, 2)))
print("Bonus awarded: " + str(bonusAwarded))

# ------------------------------------------------------------------
# Write your answers in the spaces below.
# Do not add any extra functionality to the program.
# ------------------------------------------------------------------
# 1. Name of a constant used in the program:
# 2. Name of a one-dimensional array used in the program:
# 3. Name of a two-dimensional array used in the program:
# 4. Name of a Boolean variable used in the program:
# 5. Name of a real/float variable used in the program:
# 6. Name of a user-defined function used in the program:
# 7. Line number of a selection construct:
# 8. Line number of a repetition construct:
# 9. Line number of an iteration construct:
# 10. Line number of an instruction that outputs information to the screen:

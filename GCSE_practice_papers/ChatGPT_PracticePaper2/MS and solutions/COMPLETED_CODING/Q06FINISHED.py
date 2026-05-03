# ------------------------------------------------------------------
# Q06 - Competition entry formatter
# ------------------------------------------------------------------

VALID_HOUSES = ["clare", "gonville", "pembroke", "queens"]
PASS_MARK = 50

rawEntry = ""
processedEntry = []

# ------------------------------------------------------------------
# Subprograms
# ------------------------------------------------------------------

def validateEntry(entryText):
    isValid = True
    parts = []
    nameParts = []
    codeParts = []

    entryText = entryText.strip()

    if entryText == "":
        isValid = False
    else:
        parts = entryText.split(",")

        if len(parts) != 3:
            isValid = False
        else:
            nameParts = parts[0].strip().split(" ")
            codeParts = parts[2].strip().split("-")

            if len(nameParts) < 2:
                isValid = False
            elif parts[1].strip().lower() not in VALID_HOUSES:
                isValid = False
            elif len(codeParts) != 2:
                isValid = False
            elif (len(codeParts[0]) != 2) or (not codeParts[0].isalpha()):
                isValid = False
            elif (len(codeParts[1]) != 2) or (not codeParts[1].isdigit()):
                isValid = False

    return isValid


def processEntry(entryText):
    parts = entryText.strip().split(",")
    nameParts = parts[0].strip().split(" ")
    house = parts[1].strip().lower()
    code = parts[2].strip().upper()
    codeParts = code.split("-")

    firstName = nameParts[0].lower()
    lastName = nameParts[len(nameParts) - 1].lower()
    entryID = lastName + firstName[0]
    category = codeParts[0]
    score = int(codeParts[1])

    if score >= PASS_MARK:
        status = "Accepted"
    else:
        status = "Review"

    return [entryID, house.upper(), category, score, status]


def outputTable(entryRecord):
    layout = "{:<12}{:<10}{:<10}{:>7}{:^12}"
    print(layout.format("Entry ID", "House", "Category", "Score", "Status"))
    print("-" * 51)
    print(layout.format(entryRecord[0], entryRecord[1], entryRecord[2], entryRecord[3], entryRecord[4]))

# ------------------------------------------------------------------
# Main program
# ------------------------------------------------------------------

rawEntry = input("Enter entry as full name,house,code: ")

if validateEntry(rawEntry):
    processedEntry = processEntry(rawEntry)
    outputTable(processedEntry)
else:
    print("Invalid entry")

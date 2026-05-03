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
    # ===> Write your validation code here
    return False


def processEntry(entryText):
    # ===> Write your string processing code here
    return []


def outputTable(entryRecord):
    # ===> Write your formatted output code here
    pass

# ------------------------------------------------------------------
# Main program
# ------------------------------------------------------------------

rawEntry = input("Enter entry as full name,house,code: ")

if validateEntry(rawEntry):
    processedEntry = processEntry(rawEntry)
    outputTable(processedEntry)
else:
    print("Invalid entry")

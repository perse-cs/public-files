# ------------------------------------------------------------------
# Q05 - Library membership identifier
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------

firstName = ""
lastName = ""
joinDate = ""
memberID = ""

# ------------------------------------------------------------------
# Subprograms
# ------------------------------------------------------------------

# ===> Change the names of the local variables so they are not confused
#      with the global variables with the same names.
def makeID(pFirstName, pLastName, pJoinDate):
    letterPart = ""
    numberPart = 0

    letterPart = pLastName + pFirstName[0]

    # ===> Correct the logic error caused by using int() instead of the
    #      function that returns the ASCII value of a character.
    for character in pJoinDate:
        numberPart = numberPart + ord(character)

    yourID = letterPart + str(numberPart)
    return yourID

# ===> Add a procedure, with no parameters, to display a welcome message.
def welcome():
    print("Welcome to the library membership program")

# ------------------------------------------------------------------
# Main program
# ------------------------------------------------------------------

# ===> Call the welcome procedure before taking input from the user.
welcome()

firstName = input("Enter your first name: ")
lastName = input("Enter your last name: ")

# ===> Convert the first name and last name to lowercase.
firstName = firstName.lower()
lastName = lastName.lower()

joinDate = input("Enter your joining date (ddmmyyyy): ")

# ===> Validate the joining date using a built-in string manipulation subprogram.
#      If valid, call the makeID() function and display the membership ID.
#      If invalid, display an error message and do not process the invalid input.
if (joinDate.isdigit()):
    memberID = makeID(firstName, lastName, joinDate)
    print(memberID)
else:
    print("Invalid joining date")

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
def makeID(firstName, lastName, joinDate):
    letterPart = ""
    numberPart = 0

    letterPart = lastName + firstName[0]

    # ===> Correct the logic error caused by using int() instead of the
    #      function that returns the ASCII value of a character.
    for character in joinDate:
        numberPart = numberPart + int(character)

    memberID = letterPart + str(numberPart)
    return memberID

# ===> Add a procedure, with no parameters, to display a welcome message.

# ------------------------------------------------------------------
# Main program
# ------------------------------------------------------------------

# ===> Call the welcome procedure before taking input from the user.

firstName = input("Enter your first name: ")
lastName = input("Enter your last name: ")

# ===> Convert the first name and last name to lowercase.

joinDate = input("Enter your joining date (ddmmyyyy): ")

# ===> Validate the joining date using a built-in string manipulation subprogram.
#      If valid, call the makeID() function and display the membership ID.
#      If invalid, display an error message and do not process the invalid input.

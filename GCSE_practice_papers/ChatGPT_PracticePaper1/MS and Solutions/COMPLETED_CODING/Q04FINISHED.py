# ------------------------------------------------------------------
# Q04 - Write your code below
# ------------------------------------------------------------------

# A school trip company needs a program to calculate the cost of a coach trip.
# Complete this file to meet the requirements in the question paper.

# ------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------

students = 0
adults = 0
distance = 0.0
studentCost = 0.0
adultCost = 0.0
totalCost = 0.0
layout = "Total cost: £{:>8.2f}"

# ------------------------------------------------------------------
# Main program
# ------------------------------------------------------------------

# Take and prepare inputs
students = int(input("Enter the number of students: "))
adults = int(input("Enter the number of adults: "))
distance = float(input("Enter the distance travelled: "))

# Check for invalid inputs, using relational and logical operators
if ((students <= 0) or (adults <= 0) or (distance <= 0.0)):
    print("Invalid input")
else:
    # Process all valid inputs
    studentCost = students * distance * 0.18
    adultCost = adults * distance * 0.25
    totalCost = studentCost + adultCost

    print(layout.format(totalCost))

# In all cases, display a goodbye message just before terminating
print("Goodbye")

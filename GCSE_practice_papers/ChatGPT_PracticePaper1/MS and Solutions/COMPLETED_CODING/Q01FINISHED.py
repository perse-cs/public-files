# ------------------------------------------------------------------
# Q01 - Event booking summary
# ------------------------------------------------------------------

MAX_TICKETS = 40
DISCOUNT_RATE = 0.15

workshopNames = ["Robotics", "Animation", "Cyber security", "Web design"]
placesLeft = [12, 8, 15, 5]

ticketPrice = 6.50
bookingTotal = 0.0
choice = ""


def display_workshops():
    print("Available workshops")
    for index in range(0, len(workshopNames)):
        print(str(index + 1) + ". " + workshopNames[index] + " - " + str(placesLeft[index]) + " places")


display_workshops()

while choice != "0":
    choice = input("Enter workshop number, or 0 to stop: ")

    if choice != "0":
        tickets = int(input("Enter number of tickets: "))
        bookingTotal = bookingTotal + (tickets * ticketPrice)

if bookingTotal > 25.00:
    discount = bookingTotal * DISCOUNT_RATE
else:
    discount = 0.0

finalTotal = bookingTotal - discount
print("Total to pay: £" + str(round(finalTotal, 2)))

# ------------------------------------------------------------------
# Write your answers in the spaces below.
# Do not add any extra functionality to the program.
# ------------------------------------------------------------------
# 1. Name of a constant used in the program: MAX_TICKETS
# 2. Name of a list/array used in the program: workshopNames
# 3. Name of an integer variable used in the program: tickets
# 4. Name of a real/float variable used in the program: ticketPrice
# 5. Name of a user-defined subprogram used in the program: display_workshops
# 6. Line number of a selection construct: 27
# 7. Line number of a repetition construct: 24
# 8. Line number of an iteration construct: 18

# ------------------------------------------------------------------
# Q04 - Sports hall booking calculator
# ------------------------------------------------------------------

COST_PER_COURT = 7.50
COST_PER_PLAYER = 1.25
DISCOUNT_RATE = 0.12
DISCOUNT_THRESHOLD = 45.00

courts = 0
players = 0
hours = 0.0
baseCost = 0.0
playerCost = 0.0
subtotal = 0.0
discount = 0.0
totalCost = 0.0
layout = "Total cost: £{:>8.2f}"

# Main program
courts = int(input("Enter number of courts: "))
players = int(input("Enter number of players: "))
hours = float(input("Enter number of hours: "))

if (courts <= 0) or (players <= 0) or (hours <= 0.0):
    print("Invalid input")
else:
    baseCost = courts * COST_PER_COURT * hours
    playerCost = players * COST_PER_PLAYER
    subtotal = baseCost + playerCost

    if subtotal > DISCOUNT_THRESHOLD:
        discount = subtotal * DISCOUNT_RATE
    else:
        discount = 0.0

    totalCost = subtotal - discount
    print("Subtotal: £" + str(round(subtotal, 2)))
    print("Discount: £" + str(round(discount, 2)))
    print(layout.format(totalCost))

print("Goodbye")

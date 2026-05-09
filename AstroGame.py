#Imports:
from matplotlib import pyplot as plt
import numpy as np
import time
from tabulate import tabulate

TEXT_DELAY = 1.5

def slow_print(text):
    print(text)
    time.sleep(TEXT_DELAY)

#Some variables used to lock options.
out_done = 0
chest_locked = True
filled = False


#Data needed for Hubble_constant (Whiteboard())
x1 = np.array([6.1, 14.2, 14.2, 9.8, 22.5, 19.7, 31.4, 28.0, 45.6, 41.3, 52.8, 60.2, 67.9])
y1 = np.array([800, 1200, 600, 950, 2100, 1300, 2600, 1800, 3500, 2400, 4200, 3000, 4800])
x2 = np.array([18.49, 35.48, 35.48, 11.34, 7.12, 9.82, 23.66, 44, 66.7, 52.4, 55, 25.6, 26.19])
y2 = np.array([2094.75, 2320.87, 1224.9, 872.13, 432.2, 751, 1410, 2700, 5292, 2550, 5253, 2419, 2158])
x3 = np.array([4.2, 11.5, 11.5, 7.9, 18.6, 25.3, 21.0, 37.8, 42.1, 48.9, 55.7, 63.4, 69.2])
y3 = np.array([600, 1800, 900, 1300, 3000, 2600, 3500, 5200, 4100, 5800, 4700, 6500, 6200])
x4 = 1.65*x2
y4 = -1.65*y2
x_data = [x1,x2,x3,x4]
y_data = [y1,y2,y3,y4]
title = ["A", "B", "C", "D"]

def Inside_Base():
    """Starting point of the game and leads to:
    Outside() and Lookaround()"""
    slow_print("\nYou are standing in the main hub of the research base.")
    slow_print("The hum of the generators provides a bit of comfort from the storm.")

    slow_print("\nWhat is your next move?")
    slow_print("A. Look around the room"
               "\nB. Go back outside")

    choice = input("Enter A or B: ").strip().upper()

    if choice == "A":
        # This transitions the player to your Lookaround() function
        return "LOOKAROUND"

    elif choice == "B":
        # This sends them back to the cold!
        slow_print("\nYou brace yourself and head into the wind.")
        return "OUTSIDE"

    else:
        slow_print("\nYou stand there indecisively. Pick A or B.")
        return "INSIDE"


def show_planet_terminal1():
    # 1. Define your rows
    # The first item in each list is the 'label' for that row
    row_1 = ["Position", 3, 2, 7, 4, 8, 6, 1, 5]
    if filled == False:
        row_2 = ["Planet", "Merc", "?", "Ear", "?", "Jup", "Sat", "Ura", "?"]
    else:
        row_2 = ["Planet", "Merc", "Ven", "Ear", "Mar", "Jup", "Sat", "Ura", "Nep"]
    row_3 = ["Mass (10^24 kg)", 0.3, 4.9, 6.0, 0.6, 1898, 568, 86, 102]

    table_data = [row_1, row_2, row_3]

    # 2. Use 'fancy_grid' or 'grid' for a cool retro-terminal look
    print("\n" + "=" * 50)
    print("      ACCESSING ARCHIVED PLANETARY DATA...      ")
    print("=" * 50)

    # tablefmt="fancy_grid" creates solid borders
    print(tabulate(table_data, tablefmt="fancy_grid"))

    print("=" * 50 + "\n")


def Outside():
    """Option of going outside.
    Only goes back inside."""
    global out_done # We need 'global' if we want to change this variable permanently

    if out_done == 0:
        slow_print("It's cold outside...")
        slow_print("What would you like to do?")
        slow_print("A. Walk around the base. \nB. Go back inside")
        choice = input("Fill in A or B: ").strip().upper()

        if choice == "A":
            slow_print("You see the antenna has been blown over.")
            out_done = 1  # Mark this event as finished
            return "OUTSIDE"  # Stay outside to see the 'else' text next time?

        elif choice == "B":
            return "INSIDE"  # Go back to the base

    else:
        slow_print("The wind is howling. Better go back inside.")
        return "INSIDE"


def Lookaround():
    """Option of looking around the room, leading to:
    Whiteboard(), Chest() both locked and unlocked, Coffeetable(), Launch button and going Outside()."""
    slow_print("\nYou look around the room.")
    slow_print("You see a corner with a whiteboard, a small chest, \nin the middle of the room a coffe table "
          "and the protected launch button.")
    slow_print("A. Whiteboard \nB. Small chest \nC. Coffee table  \nD. Launch button \nE. Go outside")

    choice = input("Fill in A, B, C, D or E: ").strip().upper()

    if choice == "A":
        Whiteboard() #Activates the whiteboard function.
        slow_print("Looks like they were doing research on the Hubble's constant.")
        slow_print("Maybe it can be used somewhere.")
        slow_print("I should look around more.")
        return "LOOKAROUND"  # Bring them back to the menu after they look

    elif choice == "B" and chest_locked == True: #If chest_locked == True, they haven't filled in the right password yet.
        slow_print("The chest is locked by a combination lock consisting of three numbers.")
        slow_print("You see a stickynote with the text: 'Hubble'.")
        slow_print("Want to try a code?")
        slow_print("A. Yes. \nB. No.")
        choice = input("Fill in A or B: ").strip().upper()
        if choice == "A":
            return "CHEST1" #Goes to the chest part, meaning filling in the code.
        if choice == "B":
            return "LOOKAROUND" #Goes back to the Lookaround() function.
        else:
            slow_print("You fiddle with the lock a bit. Try picking A or B")
            return "LOOKAROUND"

    elif choice == "B" and chest_locked == False:
        slow_print("The chest is still open, but you can't find more things inside of it.")
        return "LOOKAROUND"

    elif choice == "C":
        return "COFFEETABLE"

    elif choice == "D":
        return "LAUNCHBUTTON"

    elif choice == "E":
        return "OUTSIDE"

    else:
        slow_print("You stumble. Try picking A, B, C, D or E.")
        return "LOOKAROUND"

def Whiteboard():
    """Makes the plots for the whiteboard part of the game. Needed since this is part
    of the escape itself."""
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    for i, ax in enumerate(
            axes.flatten()):  # Use .flatten() to turn the 2x2 array into a 1D list of 4 items, making it easier to loop over.
        m, c = np.polyfit(x_data[i], y_data[i], 1)

        x_fit = np.linspace(x_data[i].min(), x_data[i].max(), 100)# Create the x-values for the line (from min to max of current x)
        y_fit = m * x_fit + c  # Creates the corresponding y.
        ax.set_title(title[i])  # Sets the title to one of the list.
        ax.scatter(x_data[i], y_data[i], color="cornflowerblue", label="Data Points", s=3)  # Plots the data points.
        ax.plot(x_fit, y_fit, color="orchid", label=f"$H_0$ = {m:.1f}")  # Plots the fit.
        # Setting the rest of the plots.
        ax.set_xlabel("X axis")
        ax.set_ylabel("Y axis")
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend()

    plt.tight_layout()  # Prevents labels from overlapping
    plt.show()

def Chest1():
    """This function is for filling in the combination of the locked chest, and is only called upon in said scenario.
    This function only goes back to 'LOOKAROUND'."""
    combination = input("Fill in the code.")
    global chest_locked
    if combination == "714":
        slow_print("You opened the lock!")
        slow_print("Inside you find three pictures of the planets Venus, Mars and Neptune with numbers 1-3.")
        chest_locked = False
        return "LOOKAROUND"
    elif combination != "714":
        slow_print("Wrong code. Want to try again?")
        slow_print("A. Yes. \nB. No.")
        choice = input("Fill in A or B: ").strip().upper()
        if choice == "A":
            return "CHEST1"
        if choice == "B":
            return "LOOKAROUND"

def CoffeeTable():
    """Used for the Planets part and descriptions. Leads to the planets puzzle and back to 'LOOKAROUND'."""
    slow_print("You approach the coffee table.")
    slow_print("You see two glass plates with a tabel in between.")
    slow_print("The top row shows numbers one till eight,")
    slow_print("the second row shows pictures of the planets, however some are missing,")
    slow_print("the last row shows the masses of the planets.")
    slow_print("You remember your friend telling you that the code had something to do with the masses of the planets.")
    slow_print("\nWhat do you do")
    slow_print("A.Try to solve this puzzle. \nB. Look around some more.")

    choice = input("Fill in A or B: ").strip().upper()
    if choice == "A":
        return "PLANETS"
    elif choice == "B":
        return "LOOKAROUND"



def Planets():
    show_planet_terminal1()
    global filled
    slow_print("You remember that your friend told you something about the masses having something to do with the code.")
    slow_print("You might have to solve this puzzle to get the code.")
    if chest_locked == False:
        slow_print("You remember the pictures of the planets.")
        slow_print("You add the pictures to the table")
        filled = True
        show_planet_terminal1()
        slow_print("You flip the table and notice another hint.")
        slow_print("'You have to take the first number of the masses according to the order specified'")
        slow_print("Ah that's why the planets were hidden.")
        slow_print("Lets look around some more.")
    else:
        slow_print("You can't seem to figure it out.")
        slow_print("You realize you need to look around a bit more.")
    return "LOOKAROUND"

def LaunchButton():
    slow_print("You approach the still locked launch button.")
    slow_print("You see it has a lockpad next to it with a note:")
    slow_print("'Reminder: 8-digit code!'")
    slow_print("Yeah, good reminder")
    slow_print("Want to try a code?")
    slow_print("A. Yes. \nB. No.")
    choice = input("Fill in A or B: ").strip().upper()
    if choice == "A":
        return "LAUNCHCODE"
    elif choice == "B":
        slow_print("I might need to look around more.")
        return "LOOKAROUND"
    else:
        slow_print("You stuble back. Try again later.")
        return "LOOKAROUND"

def LaunchCode():
    """This function is for filling in the combination of the keypad by the Launch Button, and is only called upon in said scenario.
        This function only goes back to 'LOOKAROUND' or 'End' if done correctly."""
    slow_print("You see the keypad blinking:")
    combination = input("Fill in the code: ")
    if combination == "84001561":
        slow_print("You see the cover around the launch button lifting.")
        slow_print("You press it and hope it worked.")
        slow_print("It's not in your hands anymore, you wish your friend the best of luck.")
        return "END"
    elif combination != "84001561":
        slow_print("Wrong code. Want to try again?")
        slow_print("A. Yes. \nB. No.")
        choice = input("Fill in A or B: ").strip().upper()
        if choice == "A":
            return "LAUNCHCODE"
        if choice == "B":
            return "LOOKAROUND"

def End():
    slow_print("A few weeks later and you get a call.")
    slow_print("'We have a call for you here at the station,")
    slow_print("please come as soon as possible.'")
    slow_print("You go to the station and who do you see on the big screen?")
    slow_print("Your friend! In space and in one piece, you did it!")
    return "QUIT"

def Quit():
    slow_print("-----------------------------")
    slow_print("That was the end of the game.")
    slow_print("Hoped you enjoyed it!")
    slow_print("-----------------------------")
    slow_print("\n\n\n")
    slow_print("The astronomical data used is:")
    slow_print("Hubble's constant: PROGNUM week 3, data")
    slow_print("Other slopes: made up by AI")
    slow_print("Masses of the planets: Nasa.") #https://ssd.jpl.nasa.gov/planets/phys_par.html
    slow_print("\n\n\n")
    slow_print("-----------------------------")

rooms = {
    "OUTSIDE": Outside,
    "INSIDE": Inside_Base,
    "LOOKAROUND": Lookaround,
    "CHEST1": Chest1,
    "COFFEETABLE": CoffeeTable,
    "PLANETS": Planets,
    "LAUNCHBUTTON": LaunchButton,
    "LAUNCHCODE": LaunchCode,
    "END": End,
    "Quit": Quit
}

#-------Start game------
slow_print("Welcome to astro escape.")
slow_print("The controls are easy.")
slow_print("When a question 'What do you do?' pops up, you'll have to make a choice.")
slow_print("This choice will be inputted in the form of A, B, C or more options.")
slow_print("You don't have to use capital letters, however you can only pick one option each time.")




slow_print("You were supposed to launch your friends rocketship,")
slow_print("however, your friend has some safety measures in place.")
slow_print("Your friend is on the phone talking you through it,")
slow_print("but right before the last code, the connection goes static.")
slow_print("You'll have to figure out the code for the keypad next to the launch button on your own.")
slow_print("You don't have a lot of time, since there is a storm brewing,")
slow_print("And the rocket needs to be launched before the storm hits them.")
slow_print("Good luck.")


current_state = "INSIDE"

while True:
    # The loop looks up "INSIDE" in the 'rooms' dictionary
    # and runs the Inside() function immediately.
    current_state = rooms[current_state]()
    #Ending the while True loop.
    if current_state == "QUIT":
        break
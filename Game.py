# ----------------- COSMIC DEAL OR NO DEAL -------------------
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys
import time
# ---------------- INPUT HANDLER & OBJECT DATA -------------------
class CosmicObject:
    def __init__ (self, name, mass):
        self.name = name
        self.mass = mass

    def info(self):
        return f"{self.name} ({self.mass:.2e} kg)"
objects = [
    CosmicObject("Asteroid", 1e12),
    CosmicObject("Moon", 7.3e22),
    CosmicObject("Mars", 6.4e23),
    CosmicObject("Earth", 6e24),
    CosmicObject("Jupiter", 1.9e27),
    CosmicObject("Sun", 2e30),
    CosmicObject("Sirius A", 4e30),
    CosmicObject("Rho Cassiopeiae", 1e31),
    CosmicObject("Sagittarius A*", 8e36),
    CosmicObject("Andromeda Galaxy", 1e42)
]
def get_input(prompt):
    """
    Handles user input, along with allowing termination
    """ 
    user_input = input(prompt).lower()

    if user_input == "cancel":
        print("\n Game terminated by user.")
        sys.exit()

    return user_input


# ---------------- INFO DISPLAY -------------------
def print_object_info(name):
    objects_info = {
        "Asteroid": {"mass": "1 × 10^12 kg", "fact": "Remnants from early Solar System."},
        "Moon": {"mass": "7.3 × 10^22 kg", "fact": "Stabilizes Earth's rotation."},
        "Mars": {"mass": "6.4 × 10^23 kg", "fact": "Home to Olympus Mons."},
        "Earth": {"mass": "6.0 × 10^24 kg", "fact": "Only known life-supporting planet."},
        "Jupiter": {"mass": "1.9 × 10^27 kg", "fact": "Largest planet in Solar System."},
        "Sun": {"mass": "2.0 × 10^30 kg", "fact": "Contains 99.8% of system mass."},
        "Sirius A": {"mass": "4.0 × 10^30 kg", "fact": "Brightest star in night sky."},
        "Rho Cassiopeiae": {"mass": "~8 × 10^31 kg", "fact": "Yellow hypergiant."},
        "Sagittarius A*": {"mass": "8 × 10^36 kg", "fact": "Black hole at galaxy center."},
        "Andromeda Galaxy": {"mass": "1 × 10^42 kg", "fact": "Heading toward Milky Way."}
    }

    print("\n--- REVEALED ---")
    time.sleep(2)
    print(name)
    print("Mass:", objects_info[name]["mass"])
    print("Fact:", objects_info[name]["fact"])

def show_available_objects(objects):
    """
    Displays all objects and their masses at the start of the game.
    """
    print("\n OBJECTS IN PLAY")
    print("-" * 35)
    for obj in objects:
        print(f"{obj.name:<18} | {obj.mass:.2e} kg")
    print("-" * 35)
# ---------------- BANKER SYSTEM -------------------
def banker_offer(available_cases, cases, round_number):
    remaining_values = [cases[i].mass for i in available_cases]
    avg_value = sum(remaining_values) / len(remaining_values)
    multiplier = 0.5 + 0.1 * round_number
    return avg_value * multiplier


def show_banker_image():
    """
    Displays the banker image when an offer is made.
    """
    try:
        img = mpimg.imread("Banker.jpg")  # putting image in same folder
        plt.imshow(img)
        plt.axis("off")
        plt.title("The Banker is Calling...")
        plt.show()
    except FileNotFoundError:
        print("(Banker image not found)")


# ---------------- GAME SETUP -------------------
cases = objects.copy()
random.shuffle(cases)

print("WELCOME TO COSMIC DEAL OR NO DEAL")
show_available_objects(objects)
# Player selects case
while True:
    try:
        player_choice = int(get_input("Choose your case (0–9, or 'cancel' if you want to end): "))
        if 0 <= player_choice < len(cases):
            break
        else:
            print("Invalid number.")
    except ValueError:
        print("Enter a valid integer.")

player_object = cases[player_choice]

print("\nYou selected your case. It remains sealed...\n")

available_cases = list(range(len(cases)))
available_cases.remove(player_choice)

cases_opened = 0
round_number = 1

# ---------------- MAIN GAME LOOP -------------------
while len(available_cases) > 1:

    print("Available cases:", available_cases)

    # Choose case
    choice = None
    while choice not in available_cases:
        try:
            choice = int(get_input("Select a case to open: "))
            if choice not in available_cases:
                print("Invalid case.")
        except ValueError:
            print("Enter a valid integer.")

    # Reveal
    revealed_name = cases[choice].name
    print_object_info(revealed_name)

    available_cases.remove(choice)
    cases_opened += 1

    # ---------------- BANKER CALL -------------------
    if cases_opened % 3 == 0: #Every 3 cases

        show_banker_image()

        offer = banker_offer(available_cases, cases, round_number)

        print("\n BANKER OFFER")
        print(f"Offer: {offer:.2e} kg")

        decision = get_input("Deal or No Deal? (deal/no): ")

        if decision == "deal":
            print("\n DEAL ACCEPTED")
            print(f"You leave with: {offer:.2e} kg")

            print("\nYour case contained:")
            print_object_info(player_object.name)
            sys.exit()

        else:
            print("\n NO DEAL — continuing...\n")
            time.sleep(2)
        round_number += 1


# ---------------- FINAL ROUND -------------------
print("\n FINAL ROUND ")

last_case = available_cases[0]

print("\nRemaining case contained:")
time.sleep(2)
print_object_info(cases[last_case].name)

print("\nYour case contained:")
time.sleep(2)
print_object_info(player_object.name)
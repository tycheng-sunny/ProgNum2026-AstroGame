#!/usr/bin/env python
# coding: utf-8

# 

# In[ ]:





# In[ ]:





# In[ ]:


import random
import time
import csv
import os
from IPython.display import clear_output

def slow_print(text: str, delay: float = 0.01) -> None:
    """
    Print text character by character with a small delay.
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def load_galaxy_data(filename="galaxy_data.csv"):
    """
    Load the astronomical galaxy data from the CSV file

    Returns
    -------
    list of dictionary
        Each dictionary contains name, type, distance, velocity.
    """
    galaxies = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            galaxies.append({
                "name": row["name"],
                "type": row["type"],
                "distance": float(row["distance_mpc"]),
                "velocity": float(row["velocity_kms"])})
    return galaxies



class Galaxy:
    """
    A class representing a galaxy as a datable character
    """

    def __init__(self, name, galtype, distance, velocity, personality):
        self.name = name
        self.type = galtype
        self.distance = distance
        self.velocity = velocity
        self.personality = personality
        self.score = 0
        self.happy = False

    def speak(self, text):
        slow_print(f" {self.name}: {text}")

    def narrate(self, text):
        slow_print(f"\n{text}")

    def choice(self, question, options):
        print("\n" + question)
        for i, opt in enumerate(options, 1):
            print(f"{i}) {opt}")

        valid = [str(i) for i in range(1, len(options) + 1)]

        while True:
            c = input("Choose your options (1,2,3) carefully, my guy: ").strip()
            if c in valid:
                return int(c) - 1
            print("Please, do not keep this lovely, exuberant, galactically beautiful galaxy waiting...")

    def interact(self):
        self.narrate(f"You find a wild {self.name}...")

        #introduction
        if self.personality == 'diva':
            self.speak("Come closer, sepeciment ") 
            options = [
                "That dust lane?? Iconic.",
                "You're glowing harder than a supernova.",
                "You're the main character of the universe."]

        elif self.personality == 'chill':
            self.speak("Yo, what brings you to my corner of the universe?")
            options = [
                "Just vibing among the stars, you know?",
                "Heard your halo was the chillest in the Local Group.",
                "Trying to escape my own galaxy's drama"]

        else:  #romantic
            self.speak("Hey... what do you want?")
            options = [
                "Are you gravity? Because I'm falling for you.",
                "You got me spiraling *wink wink*.",
                "Was that gravity or just you?"]  

        if self.choice("What do you say?", options) == 0:
            self.score += 1
            self.speak("Hmm... okay. Not bad at all")
        else:
            self.speak("...sure. I've heard worse.")

        #galaxy type
        types = ["Spiral", "Elliptical", "Irregular"]
        t = self.choice(f"{self.name}: Are you even sure I am *your* type of galaxy?", types)

        if types[t] == self.type:
            self.score += 1
            self.speak("Okay okay smart cookie, I see someone is not failling their degree")
        else:
            self.speak(f"It's {self.type}... Aren't you suppose to be an astronomy student? Yikes")

        #longdistance
        opts = [self.distance, self.distance * 2, self.distance * 0.5]
        random.shuffle(opts)
        dist_strings = [f"{o:.2f} Mpc" for o in opts]

        d = self.choice(f"{self.name}: Okay but, are you fine with our distance?", dist_strings)

        if abs(opts[d] - self.distance) < 0.3 * self.distance:
            self.score += 1
            self.speak("Long-distance relationships across cosmic scales, maybe it is worth it")
        else:
            self.speak(f"It's actually {self.distance:.2f} Mpc. Distance might not be the main issue here...")

        #doppler question
        rb = self.choice(
            f"{self.name}: Well then, what shade matches my velocity better?",
            ["Redshift", "Blueshift", "I am colorblind"])

        if rb == 2:
            self.score += 0
            self.speak("At least you're honest. Too bad, your skill issue is not an excuse.")
        elif rb == 0 and self.velocity > 0:
            self.score += 1
            self.speak("Perhaps I'm moving away from you cosmological friendzone, maybe?")
        elif rb == 1 and self.velocity < 0:
            self.score += 1
            self.speak("Finally, someone who gets Doppler shifts")  #meter outra resposta
        else:
            self.speak("Are you even trying, bro?")

        #final result
        if self.score == 4:
            self.happy = True
            self.speak("Well, well, well... I guess I found the electron to my proton, are you gonna watch me from 1 to 4 am?")
        elif self.score == 3:
            self.happy = True
            self.speak("Not THE perfect match, maybe Mercury was only half retrograte?")
        else:
            self.speak("It's going to be a big no from me. I am too much sand for your truck")


def game():
    """
    Main function to run the game
    """

    #loading the data
    data = load_galaxy_data()

    #personality types of the galaxies
    galaxies = []
    for g in data:
        if g["name"] == "Sombrero Galaxy":
            personality = "diva"
        elif g["name"] == "Andromeda":
            personality = "chill"
        else:
            personality = "romantic"

        galaxies.append(Galaxy(g["name"],g["type"],g["distance"],g["velocity"],personality))

    #introduction
    os.system('clear')
    slow_print("Did you ever catch yourself thinking...")
    input("Press Enter...")
    #clear_output()
    os.system('clear')
    slow_print("Awn man, I only enrolled in the Astronomy Degree to have a chance with those fine stellar objects...")
    input("Press Enter...")
   # clear_output()
    os.system('clear')
    slow_print("Well, this is your lucky day my dear astronomy pupil")
    input("Press Enter...")
  #  clear_output()
    os.system('clear')
    slow_print("Welcome to the Galaxy Dating Simulator, where your astronomy dreams finally come true.")  #mudar o raio do nome, tá bueda estranho
    input("Press Enter...")
    os.system('clear')
    
    results = []

    for g in galaxies:
        g.interact()
        results.append(g.happy)
        input("\n(Press Enter to continue...)")

    os.system('clear')

    #types of endings
    if all(results):
        slow_print("SUPER NOVA ENDING: You are the ultimate cosmic rizzler master.")
    elif any(results):
        slow_print("MID ENDING: You have some rizz, but the universe is vast and confusing, and so are you, maybe try the exoplanets next?")
    else:
        slow_print("BLACK HOLE ENDING: All your chances collapsed into a singularity")

if __name__ == "__main__":
    game()


# In[ ]:





# In[ ]:





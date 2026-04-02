#!/usr/bin/env python
# coding: utf-8

# In[2]:


import random
import os
from IPython.display import display, Image

# ---------- Astronomical Data ----------
STAR_DATA = [
    ("Sirius","Canis Major"),
    ("Betelgeuse","Orion"),
    ("Rigel","Orion"),
    ("Vega","Lyra"),
    ("Altair","Aquila"),
    ("Antares","Scorpius"),
    ("Polaris","Ursa Minor"),
    ("Aldebaran","Taurus"),
    ("Spica","Virgo"),
    ("Arcturus","Bootes"),
    ("Schedar","Cassiopeia"), 
    ("Alpheratz","Andromeda"),
    ("Alphard","Hydra")]

# ---------- Classes ---------------
class Star:
    def __init__(self, name, constellation):             # Initializing the class for the star (name, constellation)
        self.name = name
        self.constellation = constellation

class QuizGame:
    def __init__(self, stars, image_folder="constellation_images"):    # Initializing the class for the QuizGame
        self.stars = stars                                             # (stars, image_folder for images)
        self.image_folder = image_folder
        self.score = 0                                 # Score of user starting from 0
        self.total_asked = 0                           # Track of asked questions, starts from 0
        self.used_stars = []                           # List of stars that have been already used not to repeat them

    def get_random_star(self):                            # Getting a random star from our stated list
        if len(self.used_stars) == len(self.stars):
            self.used_stars.clear()# If all stars have been already used we start over cleaning the self.used_stars list with clear()
        available = [s for s in self.stars if s not in self.used_stars]  # Defining a list of available stars 
        # "for s (stars) in the self.stars list that are not in self.used_stars"
        chosen = random.choice(available)                                # Chosen stars from random selection 
        self.used_stars.append(chosen)                                   # Add to used stars the chosen ones
        return chosen

    def ask_question(self, star):                      # Method to generate the questions 
        print(f"\n What constellation is {star.name} in?") 
        
        answer = input().strip()                                # Answer = input(without spaces)
          # -> strip() is a Python string method that removes leading and trailing whitespace from a string. 
          # -> Whitespace includes spaces, tabs, newlines, and carriage returns.
         # My explanation: this prevents from having unnecessary spaces in the input
        
        return answer.lower() == star.constellation.lower()  # Comparing if the user's answer = the actual name of the constellation
        # .lower() converts the string into a sequence in which capital letters and small ones dont matter
        

    def show_constellation_image(self, constellation_name):                  # Method to show the constellation images 
        
        # Building the file name
        filename = constellation_name.replace(" ", "_") + ".gif"
             # replacing spaces with underscores with .replace() from the dictionary
        filepath = os.path.join(self.image_folder, filename)  # Path to show the image

        # Check if file exists just in case
        if not os.path.exists(filepath): 
            print(f"! Image not found: {filepath}")
            print("   (Make sure the image is in the 'constellation_images' folder)")
            return

        # Displaying the image
        print(f"\nConstellation: {constellation_name} ")
        display(Image(filename=filepath, width=400))

    def run(self):                                                                      # 
        print("---------------------------------------------------------------")
        print("         STAR NAME QUIZ ")
        print("---------------------------------------------------------------")
        print("I'll give you a star name, you type its constellation.")
        print("When you answer correctly, an image of the constellation will appear!\n")

        while True:   # While the game is running (it is automatically)
            star = self.get_random_star()      
            correct = self.ask_question(star)  

            if correct:
                self.score += 1
                self.total_asked += 1
                print(f" Correct! {star.name} is in {star.constellation}.")
                self.show_constellation_image(star.constellation)
                
            else:
                self.total_asked += 1
                print(f" Wrong! {star.name} is in {star.constellation}.")

            print(f"Score: {self.score}/{self.total_asked}")

            again = input("\nAnother question? (y/n): ").strip().lower()
            if again != 'y':
                break

        print("\n=========================================================")
        print(f"Final score: {self.score}/{self.total_asked}")
        print("Thanks for playing! Keep looking at the stars!")

# ---------- Main Game loop (what runs the game) ----------
stars = [Star(name, const) for name, const in STAR_DATA]   # object created (star) with variables names and constellations that takes the data from the data dictionary
game = QuizGame(stars)
game.run()


# In[ ]:





# In[ ]:





# In[ ]:





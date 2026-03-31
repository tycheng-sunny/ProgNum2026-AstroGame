#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import random
import time

class Constellation:
    """
    A class to represent and process astronomical data from FITS files.
        filename (string): name of the .fits file.
        name (string): name of the constellation.
        raw_data (array): raw data from the .fits file.
        clean_data (array): the data after noise filtering.
    """

    def __init__(self, filename, name):
        """Initializes the object and automatically loads the data."""
        self.filename = filename
        self.name = name 
        self.load_fits() #loads files immediately

    def load_fits(self):
        """Opens the fits file and handles missing file error"""
        try:
            with fits.open(self.filename) as hdul: #[0] because the primary data is in the first HDU
                self.raw_data = np.nan_to_num(hdul[0].data) #np.nan_to_num replaces non numbers with 0
        except FileNotFoundError:
            print(f"Error: {self.filename} not found!")

    def process_image(self):
        """Filters the data such that only the brightest 1% is kept"""
        cutoff = np.percentile(self.raw_data, 99) #cuts off the faintest 99% of pixels
        self.clean_data = np.where(self.raw_data > cutoff, self.raw_data, 0) #np.where replaces the faintest 99% of pixels with 0 (black)

    def display(self):
        """Displays the constellation image. The script will pause while the image window is open."""
        plt.figure(figsize=(8, 8),facecolor='black')
        plt.imshow(self.clean_data, cmap='bone', origin='lower') #origin='lower' ensures the sky isn't upside down.
        plt.title("Which constellation do you see?  Close window to guess", color='white')
        plt.axis('off') #we do not need x and y axes
        plt.show()

class ConstellationGame:
    """Manages rounds, handles guesses, and calculates scores"""

    def __init__(self, constellation_list):
        """Sets up the game score and the pool of constellations"""
        self.constellations = constellation_list
        self.score = 0

    def start(self):
        """Shuffles the deck, displays images, and gets the players input"""
        print("Welcome, in this game you have to guess which constellations you are looking at.")
        print("The 5 constellations are: Ursa Major, Ursa minor, Cassiopeia, Cygnus and Orion.")
        print()
        print("WARNING: The white stripes you might see are not stars!")
        print()
        print("The game will start automatically")
        time.sleep(12) #Pauses the game for 15 sec so the player can read the instructions
        random.shuffle(self.constellations) #shuffles the list of constellations so the game is different every time
        for i in range(5):
            print(f"\nROUND {i+1}") #/n to print on a new line
            current = self.constellations[i] #calls the constelation that is used in the loop
            current.display() #uses the display method to plot the constellation image
            guess = input("Which constellation was that? ").strip().lower() #gets the players input and make sure empty spaces and capitalization do not cause the answer to be wrong
            if guess == current.name.strip().lower(): #checks if the answer is correct
                print("Correct!")
                self.score += 1
                time.sleep(2) #gives the player time to read if their answer was correct
            else:
                print(f"Incorrect. That was {current.name}.")
                time.sleep(2)

        self.end_game() #starts the end of the game after the loop has finished

    def end_game(self):
        """Prints the final score and a perfomance based message"""
        print("\n GAME OVER ")
        print(f"Your final score: {self.score}/5")
        if self.score==5:
            print('Perfect score! Now you can impress your friends')
        elif self.score>=3:
            print('You are alright i guess.')
        else:
            print('Get to studying noob')
if __name__ == "__main__":
    # Create the library of constellation objects
    library = [
        Constellation("ursaminor.fits", "Ursa Minor"),
        Constellation("cygnus.fits", "Cygnus"),
        Constellation("cassiopeia.fits", "Cassiopeia"),
        Constellation("orion.fits", "Orion"),
        Constellation("ursamajor.fits", "Ursa Major")
    ]
    for c in library:  # Filters all images beforehand 
        c.process_image()
    game = ConstellationGame(library) #Instantiate and launch the game
    game.start()


# In[ ]:





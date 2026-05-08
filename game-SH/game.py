#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.constants import pi, G
solarmass = 1.9891*10**30

galaxynames = ["NGC7714", "NGC3169", "NGC1316", "M31", "M83", "NGC660", "M106", "M63", "NGC1566", 'M51']

class galaxy():
    """Class for the galaxy chosen by the user"""
    def __init__(self, name):
        """Initialisation function
        
        Paramaters:
            Name: String

        """
        self.name = name
        file = fits.open(f"{name}.fits")
        self.data = file[0].data

    def image(self):
        return self.data

def plot(galaxynames):
    """Function plotting all galaxies
    
    Paramters:
        galaxynames: list
        
        """
    fig, ax = plt.subplots(2, 5, figsize = (10,10))
    square = np.array(galaxynames).reshape(2,5)
    for i in range(2):
        for j in range(5):
            g = galaxy(square[i,j])
            axis = ax[i,j]
            axis.imshow(g.image())
            axis.set_title(square[i,j])
            axis.set_xticklabels([])
            axis.set_yticklabels([])
    plt.tight_layout(pad = 0.1)
    plt.show()

class star():
    
    def __init__(self, luminosity):
        self.luminosity = luminosity
        self.mass = solarmass*(luminosity)**(1/3.5)
        self.ri = 149597870700*np.sqrt(self.luminosity/1.1)
        self.ro = 149597870700*np.sqrt(self.luminosity/0.53)
    
    def distance(self, time):
        a = (G*self.mass*((time/(2*pi))**2))**(1/3)
        return a
    
    def habitable(self, a):
        if (a > self.ri) & (a < self.ro):
            return True
        else:
            return False

user = input("Hi, what's your name? ")
age = int(input("How old are you? "))
print()
ans = input(f"It is 2626, and you, {user}, are {age + 600} years old. The black hole at the center of the milkyway has decided to engulf most of it's stars, including the sun. So, yea. Sorry, there's no time to be upset, cause you, {user}, have been chosen to find us a new home. Do you accept this responsibility? ")
print()
if ans == 'yes' or ans == 'Yes':
    print("Impressive. You didn't have a choice anyways, but I respect your courage.")
else:
    print("Cute that you thought you had a choice! You don't.")
print()
print("First, choose a galaxy:")
plot(galaxynames)

choice = input("Enter the name of the galaxy you wish to choose: ")

chosenGalaxy = galaxy(choice)

print(f"Welcome to the {choice} galaxy. Take a closer look: ")
plt.imshow(chosenGalaxy.image(), cmap = "inferno")
plt.show()
print("There are plenty of stars being born here today. You can choose one based on the following parameters:")
radius = input("Enter the ideal radius of your star (in km): ")
luminosity = float(input("Enter the ideal luminosity of your star (in solar luminosities): "))
print()
print("Great! We have found you a star.")
chosenStar = star(luminosity)
print()
print(f"Now comes the hardest part, choosing a planet. Luckily you, {user}, being an astronomer, have acquired the skill of creating a planet.")
color = input("What colour would you like your planet to be? ")
name = input("Now it's time to name our future home: ")
time = 31556926*float(input(f"How long would you like one year on {name} to take? (in earth years) "))
a = chosenStar.distance(time)
print()
print(f"This will place the planet at a distance of {a:2f} m from your star...")
print("Will the planet even be habitable at this distance? did you forget what is at stake?")
print()
input("Are you ready to learn whether the planet you have chosen is habitable? ")
print("Either way, you have to face the consequences of your actions. ")
print()
h = chosenStar.habitable(a)
if h == True:
    print(f"{name} is habitable! Well done {user}, you have found a beautiful new {color} home for humanity in the {choice} galaxy. ")
else:
    print(f"{color} {name} is not habitable. You have failed us, and humanity will now go extinct. You're clearly not a very good astronomer, maybe it's time to become a business student...")
    print("Sorry, too harsh? don't worry, we'll all die soon anyways, so you won't have to suffer amongst the business students for too long :)")


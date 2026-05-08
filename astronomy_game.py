#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Task 8.1
from imageio import imwrite, imread
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure, show
import numpy as np
import time
import imageio.v2 as imageio
from PIL import Image
import time
import sys
import random
from matplotlib.animation import FuncAnimation
from matplotlib import rc
rc('animation', html='jshtml')

# defines a class that gives slowly typed output
class TypeWriter:
    def __init__(self, delay=0.05, variance=0.0):
        """
        delay: base delay between characters
        variance: random variation (+/-) to simulate human typing
        """
        self.delay = delay
        self.variance = variance

    def _get_delay(self):
        if self.variance > 0:
            return random.uniform(
                max(0, self.delay - self.variance),
                self.delay + self.variance
            )
        return self.delay

    def write(self, text, end="\n"):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(self._get_delay())
        sys.stdout.write(end)
        sys.stdout.flush()

    def writeln(self, text):
        self.write(text, end="\n")

    def pause(self, seconds):
        time.sleep(seconds)

        
# writes the introdution text using slow typing class
typer = TypeWriter(delay=0.05, variance=0.02)

typer.write("You have been selected for a secret program of the space department. The earth is dying from climate change. But there is hope. Archeologists have discovered an advanced technology that aliens left behind hundreds of years ago. This technology creates wormholes that allow us to travel to planets all over the universe. The government needs you to find a new planet for us to live.")
print()
typer.write("Here you can see a map of a distant galaxy. We have marked the known exoplanets in red, the black holes in black and supernovas in yellow. It is your job to plan a mission to one of the planets. First, you have to decide which planet we should travel to.")
            
# reads the image the galaxy
# reads the image
m101 = imread("m101BW.jpg")

# plot
fig = plt.figure(figsize=(20,20))
ax = fig.add_subplot(1,1,1)

ax.imshow(m101)
ax.set_xticks([])
ax.set_yticks([])

# markers
ax.scatter(150,150,marker='$1$', color='red', s=200)
ax.scatter(200,350,marker='$2$', color='red', s=200)
ax.scatter(300,200,marker='$3$', color='red', s=200)
ax.scatter(310,300,marker='$4$', color='red', s=200)
ax.scatter(410,300,marker='$5$', color='red', s=200)
ax.scatter(500, 235, marker='$6$', color='red', s=200)
ax.scatter(310, 260, marker='$7$', color='red', s=200)
ax.scatter(330, 300, color='black', s=200)
ax.scatter(150, 200, color='black', s=200)
ax.scatter(100, 300, marker='*', color='yellow', s=200)
ax.scatter(500, 225, marker='*', color='yellow', s=200)
ax.scatter(300, 250, marker='*', color='yellow', s=200)

plt.show()
time.sleep(2)


# lets the user choose a planet and gives feedback
while True:
    number=float(input("Enter a number to select one of the exoplanets. Consider the position of the planet. Which one seems like a safe option?: "))
    print()
    if number==6 or number==7:
        typer.write("  From our observations we know this planet is close to a star that is about to explode in a supernova. Doesn't seem very safe. Try again!")
    if number==4 or number ==1:
        typer.write("This exoplanet is too close to a blackhole. Do you really think this is an ideal enviroment for human life? Try again!")
    if number==2 or number==3 or number ==5:
        typer.write("  Good choice, your mission has been approved!")
        break

# next task
typer.write("To establish a wormhole to the selected planet we need to enter a specific code. Luckily, the aliens have left behind some hints")
print()
typer.write("The first hint that we found is an ancient text. It seems like a riddle. What number could be meant by this?")
print()
typer.write("When we look to the sky. We see five plantes circeling the sun. But the humans don't know yet that there are more. The real number of planets in this system will grant you access to the wormhole")

while True:
    c=float(input())
    if c==8:
        typer.write("Success!")
        break

    else:
        typer.write("Oh no! That was wrong.")


# introduces next task
typer.write("Great you have found the first number of the code. But we have found some more hints.")
print()
print("1  1  2  3  5  8")
typer.write("What could this mean? Can you find the next element in this sequence?: ")
print()


# lets user put in number and gives feedback
while True:
    value=float(input())
    if value==13:
        typer.write("Good job! You have found the correct value")
        break
        
    else:
        typer.write("Incorrect value. The wormhole generator is shutting down.")

typer.write("This is the next hint that we discovered. What could be the next number??")
typer.write("1  3  7  15  31")
print()
while True:
    v=float(input())
    if v==63:
        typer.write("That´s correct.")
        break

    else:
        typer.write("That seems to be wrong. We are losing control over the wormhole generator. Hurry up! You need to get it right next time")
        
print()
typer.write("Congratulations! You have successfully established a wormhole between earth and a distant planet. Now we have a chance to save humanity!")


# In[ ]:





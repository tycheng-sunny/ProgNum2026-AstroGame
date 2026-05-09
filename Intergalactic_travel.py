#!/usr/bin/env python
# coding: utf-8

# In[13]:


import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia
from astroquery.skyview import SkyView
import matplotlib.pyplot as plt
import numpy as np

# Printing the title of the game 
print("Space exploration: Venture out and find out what deep dark secrets await in the far away cosmos \n")

# Defining the variables neccessary to run the class
ra = float(input("To start off we need some parameters to narrow down our search, that is the right ascension and declination around which we'll explore! Please input a number between 0 and 360:"))
dec = float(input("Perfect, that's the right ascension. Now choose a number between -90 and 90 for the declination:"))

# Defining a class that runs the whole game
class Galaxy:
    """
    A class that is responsible for all the functions within the game.
    ...
    Attributes
    ----------
    ra : float
        right ascension in degrees, between 0 and 360
    dec : float
        declination in degrees, between -90 and 90
    Methods
    -------
    Prints the patch of sky coressponding to the coordinates.
    Pritnts a plot with the object selected by the user and information about it.
    Runs a trivia quiz.
    """
    
    def __init__(self, ra, dec):
        """
        Constructs all the necessary attributes for the person object.
        
        Parameters:
        -----------
        ra : float
            right ascension in degrees, between 0 and 360
        dec : float
            declination in degrees, between -90 and 90
        """
        self.ra = ra
        self.dec = dec
        
    def query_region(self):
        """
        Conducts a cone search through Gaia data.
        
        Returns
        -------
        A table of Gaia data for top 50 of the objects found within the cone search region.
        """
        pos = SkyCoord(self.ra, self.dec, unit="deg", frame="icrs") # defines the position in the sky in terms of ra and dec
        j = Gaia.cone_search_async(pos, radius=u.Quantity(1.0, u.deg)) # conducts a cone search of radius 1 degree from the specified coordinates
        r = j.get_results() # assigns the results of the search to r
        return r
        
    def show_image(self):
        """
        Displays an image of the sky.
        
        Returns
        -------
        An image of the sky that corresponds to the conducted cone search.
        """
        image = SkyView.get_images(position=f"{self.ra} {self.dec}",survey='DSS',radius=0.1 * u.deg) # image is an HDU list 
        im = image[0][0].data # im is the data found in the HDU list - image
        print(f"\n Let's take a closer look! Below you can see the patch of sky around the coordinates you selected.")
        fig, ax = plt.subplots()
        ax.imshow(im, cmap = 'Blues') # displays the image
        plt.show()
        
    def show_plot(self):
        """
        Displays a plot of the objects in the patch of sky.
        
        Returns
        -------
        A plot with the objects in the patch of sky, each point corresponds to the coordinates of an object,
        the arrow points to a selected by user object and the legend gives information about the object.
        """
        ra_ = self.query_region()['ra'] # data from the column ra
        dec_ = self.query_region()['dec'] # data from the column dec

        # Asking the user to choose a random object in the patch of sky
        index = int(input("\n If you wanna find out more about one of the celestial objects in the image type a number from 0 to 49:"))
        object_ra = self.query_region()['ra'][index] # ra of the chosen object
        object_dec = self.query_region()['dec'][index] # dec of the chosen object

        # Creating the scatter plot and arrow which points to the object
        fig2, ax2 = plt.subplots()
        ax2.scatter(ra_, dec_, s=5, marker = '*', color = 'white', label = f"RA: {self.query_region()['ra'][index]} \n DEC: {self.query_region()['dec'][index]} \n PARALLAX: {self.query_region()['parallax'][index]} \n NATIVE SPECIES: very chill aliens")
        ax2.annotate("Za planet", color = 'white', xy=(object_ra, object_dec), xytext=(object_ra - 0.005, object_dec - 0.005), arrowprops=dict(color='white', arrowstyle='->'))
        ax2.legend(loc = 'upper right')
        ax2.invert_xaxis() # inverting the x axis (convention is its increasing to the left)
        ax2.set_facecolor('black') # making the background black
        plt.show()
        
    def aliens(self):
        """
        Displays an alien.
        
        Returns
        -------
        An alien which dictates the conditions of the trivia.
        """
        ans = input("Do you wanna go visit? (type yes for a thrilling travel experience)")
        if ans == 'yes':
            print("""
        ⠀⠀⡠⠤⠐⠒⠂⠤⢄⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡠⠖⠁⠀⠀⠀⠀⠀⠁⠢⡈⠲⣄⠀⠀
⠀⠀⠀⠀⠀⡜⠁⠀⢀⠁⠀⠀⠈⢁⠀⠔⠀⠄⠈⢦⠀
⠀⠀⠀⠀⠀⠁⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠈⡄
⠀⠀⠀⠀⠀⣦⡇⠀⠀⠀⠀⡀⡀⠀⠀⠀⠀⠀⢸⣴⠁
⠀⠀⠀⠀⠀⢹⡧⠄⠀⠀⢉⠐⠒⠀⡉⠁⠀⠢⢼⡇⠀
⠀⠀⠀⠀⠀⢸⢸⣟⠛⣿⣦⠑⠀⠊⣴⠿⣿⣿⡏⡇⠀
⠀⠀⠀⠀⠀⠘⢮⢻⣿⣿⣿⡇⠀⢸⣿⣾⣿⣟⡴⠁⠀
⡤⠄⠀⡖⢢⠀⠈⢳⡈⠙⠛⢁⠀⡈⠛⠋⣁⡞⠁⠀⠀
⠱⡸⡀⡕⡎⠀⠀⠀⠳⣄⠀⠉⠀⠉⠀⣠⠟⠀⠀⠀⠀
⠀⢣⢣⡇⡇⠀⠀⠀⠀⠈⢧⡀⠒⢈⡼⠁⠀⠀⠀⠀⠀
⢴⢺⣃⡒⠣⡀⠀⠀⠀⠀⠸⣿⠲⣿⠇⠀⠀⠀⠀⠀⠀
⠈⠣⡹⠉⢀⠃⠀⢀⣀⡠⠜⡙⣀⢛⠣⢄⣀⡀⠀⠀⠀
⠀⠀⠑⡏⣹⠀⢸⠇⢀⠀⠉⠀⣀⠀⠁⠀⡄⠸⡆⠀⠀
⠀⠀⠀⢁⠀⢇⡸⢀⣨⡀⠀⠀⢀⠀⠀⢀⣅⠀⡇⠀⠀
⠀⠀⠀⠸⡀⠈⠇⣸⠏⣇⠀⠀⠤⠀⠀⣸⡇⠀⠀⠀⠀
⠀⠀⠀⠀⣿⡀⢨⡟⠀⡗⠀⠀⢀⠀⠀⢺⡇⠀⠇⠀⠀
⠀⠀⠀⠀⠈⠺⡽⠁⠀⠧⠬⠤⠤⠄⠄⠸⢇⣄⠇⠀
By intruding on their peaceful life you have angered the aliens of Za planet
If you answer most of their questions correctly they will spare your life,
and if not they will destroy you home planet!""")
        else:
            print("""
        ⠀⠀⡠⠤⠐⠒⠂⠤⢄⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡠⠖⠁⠀⠀⠀⠀⠀⠁⠢⡈⠲⣄⠀⠀
⠀⠀⠀⠀⠀⡜⠁⠀⢀⠁⠀⠀⠈⢁⠀⠔⠀⠄⠈⢦⠀
⠀⠀⠀⠀⠀⠁⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠈⡄
⠀⠀⠀⠀⠀⣦⡇⠀⠀⠀⠀⡀⡀⠀⠀⠀⠀⠀⢸⣴⠁
⠀⠀⠀⠀⠀⢹⡧⠄⠀⠀⢉⠐⠒⠀⡉⠁⠀⠢⢼⡇⠀
⠀⠀⠀⠀⠀⢸⢸⣟⠛⣿⣦⠑⠀⠊⣴⠿⣿⣿⡏⡇⠀
⠀⠀⠀⠀⠀⠘⢮⢻⣿⣿⣿⡇⠀⢸⣿⣾⣿⣟⡴⠁⠀
⡤⠄⠀⡖⢢⠀⠈⢳⡈⠙⠛⢁⠀⡈⠛⠋⣁⡞⠁⠀⠀
⠱⡸⡀⡕⡎⠀⠀⠀⠳⣄⠀⠉⠀⠉⠀⣠⠟⠀⠀⠀⠀
⠀⢣⢣⡇⡇⠀⠀⠀⠀⠈⢧⡀⠒⢈⡼⠁⠀⠀⠀⠀⠀
⢴⢺⣃⡒⠣⡀⠀⠀⠀⠀⠸⣿⠲⣿⠇⠀⠀⠀⠀⠀⠀
⠈⠣⡹⠉⢀⠃⠀⢀⣀⡠⠜⡙⣀⢛⠣⢄⣀⡀⠀⠀⠀
⠀⠀⠑⡏⣹⠀⢸⠇⢀⠀⠉⠀⣀⠀⠁⠀⡄⠸⡆⠀⠀
⠀⠀⠀⢁⠀⢇⡸⢀⣨⡀⠀⠀⢀⠀⠀⢀⣅⠀⡇⠀⠀
⠀⠀⠀⠸⡀⠈⠇⣸⠏⣇⠀⠀⠤⠀⠀⣸⡇⠀⠀⠀⠀
⠀⠀⠀⠀⣿⡀⢨⡟⠀⡗⠀⠀⢀⠀⠀⢺⡇⠀⠇⠀⠀
⠀⠀⠀⠀⠈⠺⡽⠁⠀⠧⠬⠤⠤⠄⠄⠸⢇⣄⠇⠀
It's too late! The aliens of Za planet noticed you trying to spy on them and are now on a vengful mission
If you answer most of their questions correctly they will spare your life,
and if not they will destroy you home planet!""")
            
    def quiz(self):
        """
        Runs a trivia.
        
        Returns
        -------
        A series of questions for the user to answer which determine whether or not you win the game.
        """
        score = [] # empty list that will store the users points
        
        ans1 = float(input("\n The first question is: What is the 100th Fibonacci number? \n"))
        if ans1 == 354224848179261915075:
            score.append(1) # if answered correctly one point gets added to the score
        
        ans2 = input("\n That one was hard I know, let's do something easier: Say i wanna reshape an array M with 10 numbers into a matrix with 2 rows and 5 columns, do i use a) M.reshape(5,2) b) np.shape(M, 2, 5) c) np.shape(M, (2,5))? Input a b or c as the asnwer \n")
        if ans2 == 'c':
            score.append(1)
        ans3 = input("""\n So far so good, time for some debugging! Which line 1-20 is the error in?

class Fibonacci:
    def __init__(self, n, m):
        self.n = n
        self.m = m
    def fibo_list(self):
        fiblist = []
        a = 0
        b = 1
        l = 1
        while l < n:
            if a > self.m and a%self.m == 0:
                fiblist.append(a)
            c = a + b
            a = b
            b = c
            l = l + 1
        return fiblist               
fib = Fibonacci(100,7)
print(fib.fibo_n())
print(fib.fibo_list()) \n""")
        
        if ans3 == 10:
            score.append(1)

        if ans3 == 10:
            score.append(1)

        ans4 = input("\n Twowo more chances to earn enough points to protect Earth from utter destruction, time to lock in! You have a data cube with  40 planes, 50 rows and 70 columns. If you wanna get a slice along the middle of the x-y plane how will you do it? Input it in the format: [,,] \n")
        if ans4 == '[:, 25, 35]' or ans4 == '[:,25,35]' or ans4 == '[ : , 25 , 35]' or ans4 == '[ : , 25, 35]':
            score.append(1)

        ans5 = input("\n Laste one! Which of these models is linear (x is the independent variable)? a) Gaussian b) Bsin(x) c) A + Be^(Bx). Input a b or c as the asnwer. \n")
        if ans5 == 'b':
            score.append(1)

        # Converting the list to an array and summing the points
        score = np.array(score)
        points = np.sum(score)

        # Printing the game ending depending on the amount of points accumulated by the user.
        if points < 3:
            print(f"""
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⣀⠀⢠⡀⣿⣰⢀⣠⠴⠋⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣙⣳⣿⣿⣿⣿⣅⣀⡀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⢠⣄⣤⣄⣠⣶⣿⡭⣙⣷⣿⣿⣿⣯⡉⠉⠁
⠀⠀⠀⠀⢀⣤⡶⠚⣿⣿⢡⣷⡻⣿⡺⡿⣻⣄⠀⣰⠟⢹⡟⣿⠀⠉⠀⠀
⠀⠀⢀⡴⠛⠙⣶⣾⣿⣿⡘⢿⣿⣷⣯⣟⣛⡟⠰⠁⠀⢸⡇⠘⡆⠀⠀⠀
⠀⢠⠏⠀⠀⣰⣿⣿⣿⣿⣿⣶⣍⣛⠻⠿⠟⣼⡆⠀⠀⢸⠃⠀⠀⠀⠀⠀
⠀⣿⣤⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠘⠂⠀⠀⠀⠀⠀
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠉⠙⠛⠛⠛⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀
YOU LOSE - your score was {points}/5, better luck next time!
(that is if you evacuate ASAP cause Earth won't be there for much longer)""")
        else:
            print(f"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣦⣄⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⢀⣠⣴⠀⠀⠀
⠀⠀⠀⠸⣿⣿⣦⣄⡀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⢀⣤⣾⣿⣿⠇⠀⠀⠀
⠀⠀⠀⠀⠹⣿⣿⣿⣿⣦⡀⠀⣿⣿⣿⣿⣿⣿⠀⢀⣴⣿⣿⣿⣿⠏⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣦⣿⣿⣿⣿⣿⣿⣴⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠠⢤⣤⣤⣤⣤⣤⣤⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣤⣤⣤⣤⣤⣤⡤⠄⠀
⠀⠀⠀⠉⠙⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠋⠉⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢈⣭⣿⣿⣿⣿⢿⡿⣿⣿⣿⣿⣭⡁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣴⣿⡿⠿⠛⠋⠁⢸⡇⠈⠙⠛⠿⢿⣿⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
YOU WON - with an impressive score of {points}/5
The aliens of Za planet accepted you as one of their own and you can visit anytime you want to chill out after the stress of PROGNUM""")
            
res = Galaxy(ra, dec)
res.query_region()
res.show_image()
res.show_plot()
res.aliens()
res.quiz()        


# In[ ]:





# In[ ]:





# In[ ]:





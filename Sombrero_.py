#!/usr/bin/env python
# coding: utf-8

# In[4]:


from astroquery.skyview import SkyView
from astropy.io import fits, ascii
from astropy.visualization import ZScaleInterval
from matplotlib import colormaps
from matplotlib.pyplot import figure, subplots, show
import numpy as np
import scipy as sc
from astroquery.simbad import Simbad
from astroquery.ipac.ned import Ned
from astroquery.sdss import SDSS



class Game:
    def __init__(self, Galaxies, Galaxy_indicies):
        
        '''This is where the first part of the game, the guessing of a random galaxy takes place
        
        parameters
        ------------------------------------------------------------
                Galaxies is the list of Galaxies with silly names
                Galaxy_indicies is the list of the 'scientific' names of these galaxies
        -------------------------------------------------------------
        returns
        -------------------------------------------------------------
        Prints the first couple lines of the game'''
        
        self.seed = np.random.randint(low = 0, high = 7, size = 1)
        print("WELCOME!!!! We are here to test what your galactic life choices are! We uhh ran out of budget so our choices are a bit slim.....\n")
        print("So, we humbly request you keep your expectations in check (pls dont sue im broke) :(")
        self.Galaxies = np.array(Galaxies)
        self.Galaxy_indicies = np.array(Galaxy_indicies)
        
    def Guess(self):
        ''' This is a simple piece of code to make the player guess which galaxy is plotted '''
        a = str(self.Galaxy_indicies[self.seed])
        a = a.strip("[]")
        corr_answ = (self.Galaxies[self.seed])
        hdu = SkyView.get_images(a[1:-1], "DSS")[0][0]
        data = hdu.data  # this is the matrix of numbers, each number = brightness of a pixel
        fig = figure(figsize=(6,6))
        ax = fig.subplots()
        interval = ZScaleInterval()
        vmin, vmax = interval.get_limits(data)
        ax.imshow(data, origin="lower", vmin = vmin, vmax = vmax)
        ax.set_axis_off()

        print("YOU ONLY GET ONCE LOOK AT THIS IMAGE!!! you're gonna have to close the window \n to make it run!")
        show()
    
        I = 0
        while I < 1000:
            I = I-1
            guess = input(f"what does this look like to you? you can guess from the following list {self.Galaxies}")
            if guess == (self.Galaxies[self.seed]):
                print("yay!")
                break
                
            else:
                print('try again!')
                I += 1

        
    
        
                
    def Word_Games(self):
        '''This function just asks a bunch of (not really) sombrero related questions about the galaxies'''
        
        common_sense = input("alright, now that you've gotten the right galaxy, do you think it actually looks like what its called?")
        if common_sense == 'no':
            print('yeah, me neither bro \n')
        else:
            print('liar.')
        print("\n --------------------------------------------- \n")
        print("we gotta do some stuff with these galaxies, icl. If we just left it as an image, what would be the point? \n", "\n We gotta play some fun games!")
        
        print('\n PLEASE USE THE INDICIES OF WHICHEVER GALAXY YOU WANT! e.g., if you want to input Sombrero, input 0')
        print(self.Galaxies)

        I = 0
        while I < 1000:
            fashion = int(input("\n which galaxy (use their indicies) do you think is the prettiest?"))
            if fashion != 0 and fashion <= 7:
                print(f"wrong choice bud, the notion of 'pretty' ISN'T subjective... and _{self.Galaxies[fashion]}_... is the WORST choice")
                I += 1
            elif fashion > 7:
                print("thats not a valid indicie")
                I += 1
            else:
                print(f"EPIC CHOICE, WE LOVEEEEEE (_{self.Galaxies[fashion]}_) IN THIS HOUSE!!\n")
                break
            
        print("          _-'-_")
        print("         /_-_-_ ")
        print(" _______|-_-_-_-|________")
        print("(________________________)")
        print(" ! ! ! ! ! ! ! ! ! ! ! ! !")

    
        print(self.Galaxies)
        while I < 1000:
            fashion = int(input("\n NEXT QUESTION!! Which galaxy has the coolest name ever?"))
            if fashion != 0 and fashion <= 7:
                print(f"ooh.. good choice, but unfortunately for you, _{self.Galaxies[fashion]}_... is the WORST choice for this")
                I +=1
            elif fashion > 7:
                print("thats not a valid indicie")
                I += 1
            else:
                print(f"Hell yeah, the Sombrero trumps all other galaxies (_{self.Galaxies[fashion]}_) !!\n")
                break
                
        print("\n NEXT QUESTION!! ")
        print(self.Galaxies)
        while I < 1000:
            fashion = int(input("\n Which of these galaxies would you be most hyped to see after drinking too much?"))
            if fashion != 0 and fashion <= 7:
                print(f"ooh.. TERRIBLE CHOICE!!! _{self.Galaxies[fashion]}_... would be MEAN to you if you got drunk smh my head")
                I +=1
            elif fashion > 7:
                print("thats not a valid indicie")
                I += 1
            else:
                print(f"The sombrero will always be there for you, dont you worry (_{self.Galaxies[fashion]}_) !!\n")
                break
        print("          _-'-_")
        print("         /_-_-_ ")
        print(" _______|-_-_-_-|________")
        print("(________________________)")
        print(" ! ! ! ! ! ! ! ! ! ! ! ! !")

        #This section is to check how many times you took to get the right answer, and prints out different results depending on how many you did get 'right'
        if I >= 3:
            print('damn you hate sombreros fr')
        elif I == 2:
            print('okay, why are you skeptical of the sombreros bruh?')
        elif I ==1:
            print('okay, okay almost a sombrero master')
        elif I == 0:
            print('oh my god its the sombrero meister themselves')
            


        
    def Serious(self):
        '''This function plots some actual astronomical stuff about the sombrero galaxy,
        namely, it plots the wavelength of the sombrero galaxy against the flux of said wavelengths
        
        returns
        ---------------------------------------------------------------------------------------------------------------
                A plot of the wavelengths against their flux is made using a NED query
                The log scales are taken to actually get usable data; we plot a vertical line at the peak wavelength
                '''
        
        print("alright, time for some serious stuff about the sombrero galaxy, lets plot the flux of different wavelengths \n for a sombrero :D From this we can discover what colour it is!")
        phot = Ned.get_table("M104", table="photometry")
        fig, ax = subplots()
        c = 3e8
        wavelength = c / phot['Frequency']
        wave = np.array(wavelength)
        photo = np.array(phot['Flux Density'])
        ax.scatter(wavelength, phot['Flux Density'])
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("Wavelength")
        ax.set_ylabel("Log of Flux Density")
        print("this gives us the intensities of different wavelengths of light present in the Sombrero galaxy, \n and shows that there is a peak between 10^-7m and 10^-3m")
        photo_new = (photo[~np.isnan(photo)])
        index = np.where(photo_new == np.max(photo_new))
        ax.axvline(wavelength[index], label = f'{float((wavelength[index])/(10**-6)):.3f}e-6m')
        ax.legend()
        print("so, our peak wavelength is in the infrared region of the electromagnetic spectrum!")
        show()

        print("So since our Sombrero is in the infrared region, we have an invisible sombrero \n Maybe... Maybe the real sombrero was the friends we made along the way")
        
    def run_game(self):
        self.Guess()
        self.Word_Games()
        self.Serious()
        

a = Game(['Sombrero', 'Tadpole', 'Evil Eye', 'Cigar', 'Cartwheel', 'Sunflower', 'Mice'], ['m104', 'UGC 10214', 'm64', 'm82', 'PGC 2248', 'm63', 'NGC 4676'])


a.run_game()


# In[ ]:





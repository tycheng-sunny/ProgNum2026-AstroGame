import numpy as np
import matplotlib
matplotlib.use('TkAgg')    #thingy to make it work in terminal
import matplotlib.pyplot as plt
from astroquery.simbad import Simbad
import astropy.units as u
from astropy.coordinates import SkyCoord


class finale:      #win sequence -- prints the full plot+sky image

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def full_plot(self):
        plt.close('all')                         #closes other one
        fig, ax = plt.subplots()
        ax.scatter(self.x, self.y, color='gold', marker='*')            #scatter+line plot
        ax.plot(self.x, self.y, lw=0.5, color='gold')
        ax.set_xlim(np.min(self.x) - 10, np.max(self.x) + 10)
        ax.set_ylim(np.min(self.y) - 10, np.max(self.y) + 10)
        ax.set_aspect('equal')
        ax.set_facecolor('midnightblue')
        plt.show(block=False)                     #doesnt wait for window to close for code to continue

    def sky_image(self):
        fig2, ax2 = plt.subplots()
        im = plt.imread(f'game_images/{self.name}.png')          #loads image from folder
        ax2.imshow(np.fliplr(im))            #flips so it matches the thingy
        ax2.axis('off')                        #no axis
        plt.show(block=True)

    def run(self, u_name):
        print(f'Congratulations {u_name}! It was {self.name}!')
        self.full_plot()
        print(f'Here is the full {self.name} constellation.')
        print(f'Here is {self.name} in the sky — do you think you could guess it from this?')
        self.sky_image()
        print(f'Thank you for playing {u_name}! Run the script again to play again.')



u_name = input('Hello! I am Jorasus a great interstellar wizard, what is your name? ')
print(f'Welcome to the Great Constellation Guessing Game {u_name}.')
print("Try and guess the constellation from the stars in the pop up plot!")
print("Your options are; orion, big dipper, cassiopeia, taurus and scorpius")
print("Type 'next' to see the next star, your constellation guess, or 'end' to end the game.")

stars = {
    'big dipper': ['Dubhe','Merak','Phecda','Megrez','Alioth','Mizar','Alkaid'],                      #lists dict with names of stars I want in the constellations
    'orion':      ['Betelgeuse','Bellatrix','Mintaka','Alnilam','Alnitak','Saiph','Rigel'],
    'cassiopeia': ['Caph','Schedar','Gamma Cas','Ruchbah','Segin'],
    'taurus':     ['Merope','Electra','Maia','Atlas','Alcyone','Gamma Tau','Delta Tau','Theta2 Tau','Epsilon Tau','Ain','Aldebaran','Zeta Tau','Elnath'],
    'scorpius':   ['Nu Sco','Beta Sco','Delta Sco','Pi Sco','Rho Sco','Sigma Sco','Antares','Tau Sco','Epsilon Sco','Mu Sco','Zeta1 Sco','Eta Sco','Theta Sco','Kappa Sco','Lesath','Shaula']
}

constellations = {}     #dict to append to

for name, star_list in stars.items():         #looping through the stars to get info (and account for processing errors)
    result = Simbad.query_objects(star_list)
    ra  = result['RA'].astype(str)
    dec = result['DEC'].astype(str)
    valid = []                   #list of valid ones to append to
    for r, d in zip(ra, dec):                   #zip goes through both of them as a tuple
        if r == 'N/A' or d == 'N/A':
            continue                           #if the processing doesnt work
        try:
            coord = SkyCoord(ra=r, dec=d, unit=(u.hourangle, u.deg))         #changing the coords
            valid.append((coord.ra.deg, coord.dec.deg))
        except Exception:                                     #accounting for error
            continue
    constellations[name] = {
        'x': [v[0] for v in valid],            #makes the dict
        'y': [v[1] for v in valid],
    }

name = np.random.choice(list(constellations.keys()))                     #chooses a random constellation and sets the x and y arrays of coords
x, y = constellations[name]['x'], constellations[name]['y']
current_stars = [1]                                                 #makes it iterable through the thing

def redraw():                              #redraws the plots
    plt.close('all')
    fig, ax = plt.subplots()
    ax.set_facecolor('black')
    ax.scatter(x[:current_stars[0]], y[:current_stars[0]], marker='*', color='gold')               #only up to the current star
    ax.set_xlim(np.min(x) - 10, np.max(x) + 10)
    ax.set_ylim(np.min(y) - 10, np.max(y) + 10)             #sets the limits so the space isnt constantly changing
    ax.set_xlabel('Right Ascension (deg)')
    ax.set_ylabel('Declination (deg)')
    ax.set_aspect('equal')              #make it equal for shape
    plt.show(block=False)              #block=false means you dont have to manually close the plot to continue, it continues anyways

redraw()          #initial thing so the first star goes

while True:                                  #loop for user input
    move = input('> ').strip().lower()                  #sign so user knows where to type - lower cased

    if move == 'next':
        if current_stars[0] < len(x):
            current_stars[0] += 1                    #calls redraw and adds to current stars
            redraw()
        else:
            print(f'Uh oh {u_name}, all the stars are already showing!')

    elif move == name:                            
        finale = finale(name, x, y)               #calls finale class
        finale.run(u_name)                        #runs all of the sequence
        break                #ends game

    elif move == 'end':                  #ends game
        print(f"Game ended. Bye bye {u_name}! Run the script again to play again.")
        plt.close('all')    #clears all plots
        break

    else:
        print(f'Wrong guess: {move}')


#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random # library for generating random integers and selections
import time # library for creating the typewriter effect and pauses
import math # library for calculating square roots for distances and spawning

def slow(text): # function to print strings one character at a time for sass
    for char in text: # iterate through every individual letter in the string
        print(char, end="", flush=True) # print character without moving to a new line
        time.sleep(0.005) # wait 5 milliseconds between each character 
    print() # print a final newline to end the line of text

class Star: # class to act as a template for stellar objects
    def __init__(self, name, abs_mag, spec, temp, color): # constructor for star properties
        self.name = name # set the common name of the star
        self.abs_mag = abs_mag # set the absolute magnitude for brightness
        self.spec = spec # set the spectral class string
        self.temp = temp # set the surface temperature in kelvin
        self.color = color # set the descriptive color for the logic puzzle

class Ship: # class to track the player's resources and position
    def __init__(self): # constructor for the ship's initial state
        self.fuel = 100 # start the player with 100 percent fuel
        self.data = 0 # start with zero out of three required scans
        self.pos = [0, 0] # start the ship at the grid center
        self.scanned_coords = set() # set to remember which tiles were already scanned

    def move(self, direction): # function to handle movement and fuel consumption
        burn = random.randint(8, 10) # random fuel cost to allow ten to twelve moves total
        self.fuel -= burn # subtract the cost from current fuel
        if direction == "w": self.pos[1] += 1 # move north on the y axis
        elif direction == "s": self.pos[1] -= 1 # move south on the y axis
        elif direction == "a": self.pos[0] -= 1 # move west on the x axis
        elif direction == "d": self.pos[0] += 1 # move east on the x axis

class Game: # main class that runs the galaxy generation and game loop
    def __init__(self): # constructor to set up the game environment
        self.ship = Ship() # create a new instance of the ship
        self.running = True # boolean flag to keep the game loop active
        self.star_pool = [ # catalogue of stars with their scientific data and colors
            Star("Sirius A", 1.42, "A1V", 9940, "White"), 
            Star("Canopus", -5.53, "A9II", 7350, "White"),
            Star("Rigel", -7.84, "B8Ia", 12100, "Blue-White"), 
            Star("Betelgeuse", -5.85, "M1Ia", 3500, "Red"),
            Star("Vega", 0.58, "A0V", 9600, "White"), 
            Star("Arcturus", -0.31, "K1III", 4290, "Orange"),
            Star("Capella", -0.48, "G3III", 4970, "Yellow"), 
            Star("Procyon", 2.66, "F5IV", 6530, "Yellow-White"),
            Star("Achernar", -2.77, "B6V", 15000, "Blue-White"), 
            Star("Altair", 2.22, "A7V", 7700, "White"),
            Star("Aldebaran", -0.63, "K5III", 3910, "Orange"), 
            Star("Spica", -3.55, "B1V", 22400, "Blue"),
            Star("Antares", -5.28, "M1Ib", 3400, "Red"), 
            Star("Pollux", 1.09, "K0III", 4660, "Orange"),
            Star("Deneb", -8.38, "A2Ia", 8500, "White"), 
            Star("Regulus", -0.52, "B7V", 10300, "Blue-White"),
            Star("Adhara", -4.11, "B2II", 22200, "Blue"), 
            Star("Castor", 0.59, "A1V", 9300, "White"),
            Star("Shaula", -5.05, "B2IV", 25000, "Blue"), 
            Star("Bellatrix", -2.78, "B2III", 22000, "Blue"),
            Star("Elnath", -1.37, "B7III", 13600, "Blue-White"), 
            Star("Miaplacidus", -1.03, "A2IV", 8866, "White"),
            Star("Alnilam", -6.37, "B0Ia", 27000, "Blue"), 
            Star("Alnair", 2.15, "B6V", 13500, "Blue-White"),
            Star("Alnitak", -5.25, "O9Ib", 29500, "Blue"), 
            Star("Alioth", -0.21, "A1III", 9080, "White"),
            Star("Dubhe", -1.10, "K0III", 4660, "Orange"), 
            Star("Mirfak", -4.50, "F5Ib", 6350, "Yellow-White"),
            Star("Fomalhaut", 1.74, "A3V", 8590, "White"), 
            Star("Polaris", -3.64, "F7Ib", 6015, "Yellow-White")
        ] # end of the comprehensive star data list
        self.star_map = {} # dictionary to map coordinates to star objects
        self.generate_map() # call the procedural map generator

    def generate_map(self): # function to place stars randomly with central bias
        stars_to_spawn = random.sample(self.star_pool, 15) # pick fifteen unique stars from the pool
        for star in stars_to_spawn: # loop through each selected star
            placed = False # initialize placement flag as false
            for attempt in range(100): # attempt to find a valid spot 100 times
                rx, ry = random.randint(-5, 5), random.randint(-5, 5) # generate random coordinates
                dist = math.sqrt(rx**2 + ry**2) # calculate distance from center using pythagoras
                if (rx, ry) not in self.star_map and random.uniform(0, 5) > dist: # check for overlap and bias
                    self.star_map[(rx, ry)] = star # assign the star to the map dictionary
                    placed = True # set placement flag to true
                    break # exit the attempt loop for this star
            if not placed: # if the biased placement failed after 100 tries
                self.star_map[(random.randint(-1,1), random.randint(-1,1))] = star # force placement near center

    def get_closest_dist(self): # logic to calculate the nearest star distance
        if not self.star_map: return 0 # return zero if no stars remain on map
        distances = [math.sqrt((sx-self.ship.pos[0])**2 + (sy-self.ship.pos[1])**2) for (sx,sy) in self.star_map] # list distances
        return min(distances) # return the smallest distance value found

    def show_hud(self): # function to display the ship status and sensors
        print("\n" + "—"*55) # print a long horizontal divider line
        slow(f"Fuel: {self.ship.fuel}% | Scientific logs: {self.ship.data}/3") # show fuel and progress
        slow(f"Grid loc: [x: {self.ship.pos[0]}, y: {self.ship.pos[1]}]") # show current coordinates
        near = self.get_closest_dist() # retrieve the distance to the nearest signal
        if near == 0: slow("Sensor: You are floating right on top of a signal. Try to pay attention.") # sass for being on target
        else: slow(f"Sensor: There is a faint signal {near:.2f} units away. Or it's a smudge on the lens.") # sass for proximity
        print("—"*55) # print the closing horizontal divider line

    def scan(self): # the puzzle logic for identifying a star
        loc = (self.ship.pos[0], self.ship.pos[1]) # store current location as a tuple
        if loc in self.ship.scanned_coords: # check if this spot was already scanned
            slow("\n[!] We have already analyzed this void. My memory banks are not the problem here.") # sass for re-scanning
            return # exit the scan function early
        if loc in self.star_map: # check if there is actually a star at this location
            target = self.star_map[loc] # identify the target star object
            slow(f"\n[!] Signal acquired. Analyzing data stream...") # announce detection
            slow(f"Spectral Type: {target.spec}") # display the spectral classification code
            slow(f"Temperature: {target.temp}K") # display the surface temperature in kelvin
            decoys = random.sample([s for s in self.star_pool if s != target], 2) # pick two incorrect stars
            options = decoys + [target] # combine decoys and target into a list
            random.shuffle(options) # shuffle the list to randomize answer positions
            slow("Identify the source based on the estimated color profile:") # prompt the player
            for i, opt in enumerate(options): # loop through the randomized choices
                print(f"{i+1}. {opt.name} ({opt.color} Star)") # display option number, name, and color
            ans = input("\nSelection: ") # capture user input for the quiz
            if ans.isdigit() and 1 <= int(ans) <= 3 and options[int(ans)-1] == target: # check if answer is correct
                gain = random.randint(6, 7) # calculate a small random fuel reward
                self.ship.fuel = min(100, self.ship.fuel + gain) # add fuel to ship without exceeding capacity
                slow(f">> Correct. Siphoning {gain}% fuel from stellar radiation. Better than nothing.") # success sass
                self.ship.data += 1 # increment the count of collected logs
                del self.star_map[loc] # remove the discovered star from the map
            else: # handle incorrect answers
                slow(">> Incorrect. That was a solar flare, or perhaps just your intuition failing again.") # failure sass
            self.ship.scanned_coords.add(loc) # record the coordinate as explored
        else: # handle scans in empty space
            slow("\n[?] Scan complete. There is nothing here but cosmic dust and my growing impatience.") # empty scan sass
            self.ship.scanned_coords.add(loc) # record the empty coordinate as explored

    def play(self): # the core game engine and user interaction loop
        slow("Astra-1: Sector initialized. I have detected 15 signals. We only need 3.") # intro message
        slow("Our fuel is finite. Do try to move with a sense of purpose.") # initial sass
        while self.running: # keep looping as long as the game is active
            self.show_hud() # update and display the head-up display
            if (abs(self.ship.pos[0]) > 5 or abs(self.ship.pos[1]) > 5): # check for boundary exit
                slow("\nLeaving the mission sector? Bold choice. Enjoy the infinite darkness.") # exit sass
                break # break the loop and end the game
            if self.ship.fuel <= 0: # check if fuel has run out
                slow("\nFuel depleted. We are now a very expensive piece of space debris. Goodbye, pilot.") # fuel loss sass
                break # break the loop and end the game
            if self.ship.data >= 3: # check if the win condition is met
                slow("\nThree logs archived. We can go home now. I will start the paperwork.") # victory sass
                break # break the loop and end the game
            last_pos = (self.ship.pos[0], self.ship.pos[1]) # remember position before moving
            cmd = input("\n[1] Scan [wasd] Move [q] Quit: ").lower() # get user command
            if cmd == "1": # check for scan command
                self.scan() # call the scan function
            elif cmd in ["w", "a", "s", "d"]: # check for movement commands
                self.ship.move(cmd) # execute movement logic
                if last_pos in self.star_map and last_pos not in self.ship.scanned_coords: # check for missed star
                    slow("\n[!] You just flew right over a signal. I suppose looking at the sensors is optional for you.") # miss sass
            elif cmd == "q": # check for quit command
                slow("\nAborting mission. I will tell command you just werent up for it.") # quit sass
                self.running = False # set running to false to end the loop

if __name__ == "__main__": # standard entry point for the python script
    app = Game() # create the game application object
    app.play() # begin the gameplay loop


# In[ ]:





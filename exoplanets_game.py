#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
import time
import sys



class Exoplanet:
    """
    Represents a distant world and its physical properties.
    """
    def __init__(self, name, star_type, temp, radius, habitable):
        # Initiate variable names
        self.name = name
        self.star_type = star_type
        self.temp = int(temp)           # Temperature in Celsius
        self.radius = float(radius)     # Earth Radii (1.0 = Earth size)
        self.is_actually_habitable = habitable == "yes" # Planet is habitable when habitable (the argument) is True

    def display_relevant_info(self):
        """
        Prints a detailed report of the planet's physical characteristics.
        Units: Temperature in Celsius, Radius in Earth Radii.
        """
        print(f"\n---SCANNING: {self.name}---")
        print(f"Spectral Type: {self.star_type}")
        print(f"Equilibrium Surface Temperature: {self.temp}")
        print(f"Radius: {self.radius}")


        
        


class ExoplanetsExplorationGame:
    """
    Handles the CSV data file, interactions with users, records scoring...(-> Game Engine)
    """
    
    def __init__(self, filename):
        """
        Initialises mission
        """
        self.filename = filename
        self.score = 0
        self.planets = []     # Create a list that will contain the exoplanets
        self.probes = 4       # Resource management: 4 probes for 10 planets

    def load_planet_data(self):
        """
        Reads CSV
        """
        try:
            with open(self.filename, mode='r') as f:
                reader = csv.DictReader(f)
                for row in reader:     # Create the objects for Exoplanet(the class)
                    p = Exoplanet(row['name'], row['star_type'], row['temp'], row['radius'], row['habitable'])
                    self.planets.append(p)

        except FileNotFoundError:
            print(f"CRITICAL ERROR: Data file '{self.filename}' not found.")
            sys.exit() # If FileNotFoundError happens, sys.exit() stops the code from running so that a "python" error message does not appear

    def run_mission(self):
        """
        The main game loop.
        """
        print("-----------------------------------------------")
        print("  KAPTEYN INSTITUTE FOR ASTRONOMY - CLI")
        print("  DEEP SPACE HABITABILITY SCANNER v1.0")
        print("-----------------------------------------------")
        print("Mission: Evaluate 10 targets for colonization.")
        print(f"Resources: {self.probes} High-Resolution Probes.")
        time.sleep(1)

        # Step 1: Load the data first
        self.load_planet_data() 

        # Step 2: Loop through the planets
        for planet in self.planets:
            if self.probes <= 0:
                print("\n[SYSTEM] No more probes available. Mission terminated.")
                break

            planet.display_relevant_info() 
            print(f"Status: {self.probes} Probes remaining.")
            
            decision = input("Authorize probe deployment(yes/no)?: ").lower()

            if decision == 'yes':
                self.probes -= 1
                print(">>> Deploying probe... analyzing atmospheric composition.")
                time.sleep(2) # Player waits while probe is "deploying"

                if planet.is_actually_habitable:
                    print(">>> SUCCESS: Planet confirmed as habitable.")
                    print(">>> SCIENCE POINTS: +100")
                    self.score += 100
                else:
                    print(">>> FAILURE: Environment is hostile. Probe destroyed.")
                    print(">>> SCIENCE POINTS: -50")
                    self.score -= 50
            else:
                print(">>> Target bypassed. Moving to next coordinate.")
        
        # Step 3: Show the summary after the loop finishes
        self.display_summary()

    def display_summary(self):
        """
        Prints the final scientific performance report
        """
        print("\n" + "#"*45)
        print("          FINAL MISSION SUMMARY")
        print("#"*45)
        
        print(f" Final Scientific Score: {self.score}")
        print(f" Remaining Probes: {self.probes}")

        if self.score >= 200:
            print(" EVALUATION: Mission Successful. Excellent analysis.")
        else:
            print(" EVALUATION: Mission Incomplete. Better luck next time.")
        print("#"*45)


# This block starts the program
if __name__ == "__main__":
    my_mission = ExoplanetsExplorationGame('exoplanets.csv')
    my_mission.run_mission()


    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





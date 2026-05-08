#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt
import numpy as np

"""About calling the player's star: 
    Use self when inside Star class
    Use star or player_star when in another class and the star is passed to the class
    Use updated_star when receiving the star back from a method """

""" -------------------------------------------- Star Database ------------------------------------------------"""
class StarDatabase:
    """Database with stars"""
    
    def __init__(self):
        
        self.stars = self.database()
        self.star_names = list(self.stars.keys())   # list of star names
    
    def database(self):
        """
        Masses are given in solar masses, luminosities in solar luminosities

        source: Stellar Catalog (stellarcatalog.com)
        
        """
        
        stars = {}
        
        stars['Sirius A'] = {'mass': 2.06, 'luminosity': 25.4, 'type': "A-type"}
        stars['Sirius B'] = {'mass': 1.02, 'luminosity':0.056, 'type': "White Dwarf" }
        stars['Proxima Centauri'] = {'mass': 0.12, 'luminosity':0.00005, 'type': "Red Dwarf"}
        stars['Alpha Centauri A'] = {'mass': 1.1, 'luminosity':1.5, 'type':"G-type" }
        stars['Alpha Centauri B'] = {'mass': 0.9, 'luminosity':0.5, 'type':"K-type" }
        stars['Altair'] = {'mass': 1.79, 'luminosity':10.6, 'type':"A-type" }
        stars['Betelgeuse'] = {'mass': 15.0, 'luminosity': 126000, 'type': "Red Supergiant"}
        stars['Rigel'] = {'mass': 21.0, 'luminosity':120000, 'type': "Blue Supergiant"}
        stars['Antares'] = {'mass': 12.0, 'luminosity': 65000, 'type':"Red Supergiant" }
        stars['Polaris'] = {'mass': 5.4, 'luminosity': 2500, 'type': "Cepheid Variable"}
        stars['Vega'] = {'mass':2.1 , 'luminosity':40.1, 'type': "A-type"}
        stars['Deneb'] = {'mass': 19.0, 'luminosity': 196000, 'type': "Blue Supergiant"}
        stars['Arcturus'] = {'mass': 1.1, 'luminosity': 170, 'type': "K-type Giant"}
        stars["Barnard's Star"] = {'mass': 0.15, 'luminosity':0.0004, 'type': "Red Dwarf"}
        
        return stars
    
    def get_random_star(self):
        """Get a random star from the database"""
        star_names = np.random.choice(self.star_names)   # Get a random name
        star_data = self.stars[star_names]    # Get the data for that name

        random_star = {                  # Dictionary with the attacking star info
            'name' : star_names,
            'mass' : star_data['mass'],
            'luminosity' : star_data['luminosity'],
            'type': star_data['type']
        }
        
        return random_star

""" -------------------------------------------- Encounter other Stars ------------------------------------------------"""

class StellarEncounter:
    """ Player's star encounters another star from the database """
    
    def __init__(self, database):
        self.database = database
        self.attack_star = database.get_random_star()     # define the random star from the database
    
    def encounter_approach(self, player_star, player_choice):
        """ The encounter is shaped by what the player chooses """
        
        if player_choice == "1":
            # Aggressive approach (try to dominate)
            return self.aggressive_approach(player_star)
            
        elif player_choice == "2":
            # Evasive approach (try to escape)
            return self.evasive_approach(player_star)
            
        else:
            # Balanced approach (let properties decide)
            return self.balanced_approach(player_star)

    """ For the approaches: 

    There is a specific chance to win, depending on star's properties. If success, player can gain mass/luminosity/velocity.
    Aggressive: based on mass and luminosity
    Evasive: based on velocity
    Balanced: based on all properties

    If success, the method returns True
    If loses, the method returns False

    Methods return also message and updated player star info
    """
    
    def aggressive_approach(self, player_star): 
        """Try to dominate the encounter using superior mass"""
        
        # Success chance based on mass and luminosity ratio
        mass_ratio = player_star.mass / self.attack_star["mass"]
        lum_ratio = player_star.luminosity / self.attack_star["luminosity"]
        
        """ Higher mass and luminosity increase success chance
        Base chance = 20
        Mass contributes up to 30% success
        (e.g. if your star is 2x more massive than opposing, then 60% chance added (but capped at 90%))
        Luminosity contribution up to 20%
        Chance capped at 90%
        """
        success_chance = min(90, 20 + (mass_ratio * 30) + (lum_ratio * 20))

        # pick random integer 1-100, if success_chance is bigger than that number -> victory
        outcome = np.random.randint(1, 101)
        
        if outcome <= success_chance:  # If success: gain mass or luminosity
            
            mass_gain = self.attack_star["mass"] * np.random.uniform(0.05, 0.15)   # gain btwn 5-15 % more from other star
            lum_gain = self.attack_star["luminosity"] * np.random.uniform(0.05, 0.15)    # gain btwn 5-15%
            
            player_star.mass += mass_gain
            player_star.luminosity += lum_gain
            player_star.lifetime = player_star.calculate_lifetime()    # calculate lifetime again
            
            message = f"""
╔══════════════════════════════════════════════════════════╗
║                        VICTORY!                          ║
╚══════════════════════════════════════════════════════════╝

{player_star.name} completely crushed {self.attack_star['name']}!

{player_star.name} absorbed material from the encounter!
   • Mass increased by +{mass_gain:.2f} M☉
   • Luminosity increased by +{lum_gain:.2f}

{player_star.name} is now stronger than before!
"""
            return True, message, player_star
            
        else:      # Failure
            
            message = f"""
╔══════════════════════════════════════════════════════════╗
║                        DEFEAT!                           ║
╚══════════════════════════════════════════════════════════╝

{player_star.name} was destroyed by {self.attack_star['name']}!

The gravitational force of {self.attack_star['name']} tore {player_star.name} apart.

GAME OVER 
"""
            return False, message, player_star
    
    def evasive_approach(self, player_star):
        """Try to escape the encounter"""
        # Escape chance based on velocity

        """  
        Base chance = 25%
        velocity ratio = (velocity in km/s) / 60 -> to get 0 to 1
        chance = base + velocity ratio*50

        e.g. velocity is 30 km/s -> ratio: 0.5 -> chance = 25%
        """
        
        escape_chance = min(90, 25 + (player_star.velocity / 60) * 50)

        outcome = np.random.randint(1, 101)
        
        if outcome <= escape_chance:
            
            v_increase = np.random.uniform(0.05, 0.10)*player_star.velocity   # increase = 5-10% more velocity from base velocity
            player_star.velocity += v_increase
            player_star.lifetime = player_star.calculate_lifetime()
            
            message = f"""
╔══════════════════════════════════════════════════════════╗
║                        ESCAPE!                           ║
╚══════════════════════════════════════════════════════════╝

{player_star.name} narrowly escaped {self.attack_star['name']}!

The rush from your escape increased your velocity!
   • Velocity increased by +{v_increase:.2f} km/s

{player_star.name} lives to see another day!
"""
            return True, message, player_star
 
        elif outcome <= (escape_chance + 15):    # not enough to survive, but add 15% -> survives but damage

            mass_loss = player_star.mass * np.random.uniform(0.05, 0.10)   # 5-10%% loss
            lum_loss = player_star.luminosity * np.random.uniform(0.05, 0.10)
            
            player_star.mass -= mass_loss
            player_star.luminosity -= lum_loss
            player_star.lifetime = player_star.calculate_lifetime()
            
            message = f"""
╔══════════════════════════════════════════════════════════╗
║                         DAMAGE!                          ║
╚══════════════════════════════════════════════════════════╝

{player_star.name} was caught in {self.attack_star['name']}'s gravity!

{player_star.name} suffered damage but survived:
   • Mass decreased by -{mass_loss:.2f} M☉
   • Luminosity decreased by -{lum_loss:.2f}

{player_star.name} is weakened but still alive!
"""
            return True, message, player_star

        else:
            # loses, Game over
            message = f"""
╔══════════════════════════════════════════════════════════╗
║                         DEFEAT!                          ║
╚══════════════════════════════════════════════════════════╝

{player_star.name} was pulled in by {self.attack_star['name']}'s gravity!

The gravitational forces tore {player_star.name} apart.

GAME OVER
"""
            return False, message, player_star
            
    
    def balanced_approach(self, player_star):
        """ Based on all properties. Player can either win and gain/lose properties, or they can lose the game"""

        mass_ratio = player_star.mass / self.attack_star["mass"]
        velocity_ratio = player_star.velocity / 60
        
        # Higher mass and velocity increase survival chance
        survival_chance = min(90, 20 + (mass_ratio * 25) + (velocity_ratio * 25))

        # (Base chance 20%) + (25% * mass ratio) + (25% * velocity ratio)

        outcome = np.random.randint(1, 101)
        
        if outcome <= survival_chance:   # Player won, but let's now see if they gain/lose properties

            # If player star is bigger than attack star: mass_ratio > 1
            
            if mass_ratio > 1:
                # Slight gain
                mass_change = self.attack_star["mass"] * np.random.uniform(0.05, 0.10)
                lum_change = self.attack_star["luminosity"] * np.random.uniform(0.05, 0.10)
                player_star.mass += mass_change
                player_star.luminosity += lum_change
                gain = "gained"
                
            else:
                # Slight loss
                mass_change = player_star.mass * np.random.uniform(0.05, 0.10)
                lum_change = player_star.luminosity * np.random.uniform(0.05, 0.10)
                player_star.mass -= mass_change
                player_star.luminosity -= lum_change
                gain = "lost"
            
            player_star.lifetime = player_star.calculate_lifetime()
            
            message = f"""
╔══════════════════════════════════════════════════════════╗
║                         SURVIVAL!                        ║
╚══════════════════════════════════════════════════════════╝

{player_star.name} had a close encounter with {self.attack_star['name']}!

{player_star.name} {gain} some material:
   • Mass: {gain} {mass_change:.2f} M☉
   • Luminosity: {gain} {lum_change:.2f}

The collision was dramatic but {player_star.name} survived!
"""
            return True, message, player_star
            
        else:

            message = f"""
╔══════════════════════════════════════════════════════════╗
║                         DEFEAT!                          ║
╚══════════════════════════════════════════════════════════╝

{player_star.name} was completely destroyed by {self.attack_star['name']}!

The collision was catastrophic.

GAME OVER
"""
            return False, message, player_star

""" ----------------------------------------- STAR DESCRIPTION AND PROPERTIES -------------------------------- """

class Star:
    """ Player designs their own star """

    def __init__(self, mass, luminosity, velocity, name):
        self.mass = mass               # in solar masses
        self.luminosity = luminosity   # in solar luminosities
        self.velocity = velocity       # km/s
        self.lifetime = self.calculate_lifetime()    # computed from mass and luminosity, not a fundamental property so not a variable
        self.name = name

    def calculate_lifetime(self):
        """ t = (M/L)*T_sun where t_sun = 10 billion years """

        t_sun = 10
        
        return (self.mass / self.luminosity)*t_sun

    def spectral_type(self):
        """ Determine spectral class based on mass in solar masses"""
        
        if self.mass >= 15:
            return "O"
        elif self.mass >= 2.1 and self.mass < 15:
            return "B"
        elif self.mass >= 1.4 and self.mass < 2.1 :
            return "A"
        elif self.mass >= 1.04 and self.mass < 1.4:
            return "F"
        elif self.mass >= 0.8 and self.mass < 1.04:
            return "G"
        elif self.mass >= 0.45 and self.mass < 0.8:
            return "K"
        else:
            return "M"

    def classify_star(self):
        """ Determine star type """
        
        if self.mass >= 15:
            return "Blue Supergiant"
        elif self.mass >= 8:
            return "Blue Giant"
        elif self.mass >= 2.1:
            return "B-type Main Sequence Star"
        elif self.mass >= 1.4:
            return "A-type Main Sequence Star"
        elif self.mass >= 1.04:
            return "F-type Main Sequence Star"
        elif self.mass >= 0.8:
            return "G-type Main Sequence Star (Sun-like)"
        elif self.mass >= 0.45:
            return "K-type Main Sequence Star"
        else:
            return "Red Dwarf"


    def star_description(self):
        """ Return a descriptive text based on mass, luminosity, and velocity """
        
        # Mass-based description
        if self.mass >= 15:
            mass_desc = "a supermassive star, extremely bright and hot"
            fate_desc = "and will collapse into a black hole"
            lifetime_desc = "will live just a few million years"
        elif self.mass >= 8:
            mass_desc = "an extremely massive star, very hot and very luminous"
            fate_desc = "and will explode as a supernova"
            lifetime_desc = "will live only a few million years"
        elif self.mass >= 2.1:
            mass_desc = "a massive main sequence star, hot and very luminous"
            fate_desc = "and will end as a supernova"
            lifetime_desc = "will live for a few tens of millions of years"
        elif self.mass >= 1.4:
            mass_desc = "a white A-type main sequence star, hot and luminous"
            fate_desc = "and will end as a supernova"
            lifetime_desc = "will live for a few hundred millions of years"
        elif self.mass >= 1.04:
            mass_desc = "a yellow F-type main sequence star, warm and bright"
            fate_desc = "and will end as a supernova"
            lifetime_desc = "will live for a few tens of millions of years"
        elif self.mass >= 0.8:
            mass_desc = "a sun-like, main sequence star, stable and yellow"
            fate_desc = "and will become a white dwarf"
            lifetime_desc = "will live around 10 billion years"
        elif self.mass >= 0.45:
            mass_desc = "an orange K-type main sequence star, cool and stable"
            fate_desc = "and will become a dwarf"
            lifetime_desc = "will live for tens of billions of years"
        else:
            mass_desc = "a small red dwarf, dim and cool"
            fate_desc = "and will fade quietly into a white dwarf"
            lifetime_desc = "will live trillions of years"
    
        # Luminosity-based
        if self.luminosity < 20:
            lum_desc = "It glows faintly in the night sky"
        elif self.luminosity < 100:
            lum_desc = "It shines brightly and its light dominates the surroundings"
        else:
            lum_desc = "It shines with extreme brilliance, blinding all other stars"

        # Velocity-based 
        if self.velocity < 10:
            vel_desc = "It drifts slowly through its galaxy at a languid pace, just admiring the cosmos."
        elif self.velocity < 25:
            vel_desc = "It moves at a moderate speed through space, not in a rush but not lazing about either."
        else:
            vel_desc = "It rockets rapidly through the galaxy! Luckily there are no speeding laws in space."
        
        description = f"""DESCRIPTION OF YOUR STAR:
══════════════════════════════════════════════════════════
                       {self.name}    
 Type : {self.classify_star()}
 Spectral Type : {self.spectral_type()}
 Mass : {self.mass:.2f} M☉
 Luminosity : {self.luminosity:.2f} L☉
 Velocity : {self.velocity} km/s
 Lifetime : {self.calculate_lifetime():.2f} billion years

{self.name} is {mass_desc}. {lum_desc}. 
{vel_desc}
{self.name} {lifetime_desc}, {fate_desc}.
══════════════════════════════════════════════════════════
"""
        print(description)
        
        return description
        
    def star_summary(self):
        
        summary = f"""══════════════════════════════════════════════════════════
 Type : {self.classify_star()}                            
 Spectral Type : {self.spectral_type()}                  
 Mass : {self.mass:.2f} M☉                                
 Luminosity : {self.luminosity:.2f} L☉                      
 Velocity : {self.velocity:.2f} km/s                          
 Lifetime : {self.calculate_lifetime():.2f} billion years 
══════════════════════════════════════════════════════════"""  
        print(summary)
        
        return summary

    def get_colour(self):
        """ Spectral type dictates visual colour (some colours are using html hex colours)"""
        if self.mass >= 15:
            return "blue"          # Blue Supergiant
        elif self.mass >= 8:
            return "#4B0082"       # Indigo Blue - Blue Giant
        elif self.mass >= 2.1:
            return "#ADD8E6"       # Light Blue - B-type
        elif self.mass >= 1.4:
            return "white"         # White - A-type
        elif self.mass >= 1.04:
            return "#FFFACD"       # Light Yellow - F-type
        elif self.mass >= 0.8:
            return "yellow"        # Yellow - G-type (Sun-like)
        elif self.mass >= 0.45:
            return "orange"        # Orange - K-type
        else:
            return "red"           # Red - M-type (Red Dwarf)

    def draw(self):
        """A drawing of the star"""
        import math

        plt.style.use('dark_background')

        fig = plt.figure(figsize=(4,4))
        ax = fig.add_subplot(1,1,1, aspect='equal')

        print(f"Look how cute {self.name} is!\n")

        # Sizing based on mass (in pixels)
        
        if self.mass >= 15:
            size = 120           # Supergiant
        elif self.mass >= 8:
            size = 100           # Giant
        elif self.mass >= 1.04:
            size = 80            # Main Sequence
        elif self.mass >= 0.45:
            size = 60   # K-type Main Sequence (Sun-like)
        else:
            size = 40   # Red Dwarf

        colour = self.get_colour()

        # Add glow effect
        for i in range(5, 0, -1):
            glow = plt.Circle((0, 0), size + i * 10,
                              color=colour, alpha=0.05*i)
            ax.add_patch(glow)

        # Star Design (circle)
        star_circle = plt.Circle((0, 0), size, color=colour, zorder=10)
        ax.add_patch(star_circle)
    
        ax.set_xlim(-240, 240)
        ax.set_ylim(-240, 240)
        ax.set_title(f"{self.name}\ntype {self.spectral_type()}, {self.classify_star()}")
        ax.axis('off')
        
        plt.show()

""" ----------------------------------------------- GAME MECHANICS -----------------------------------------------------"""

# this class depends on all the classes above, which is why it's last
class Game:
    def __init__(self):
        self.coins = 100
        self.mass = None
        self.luminosity = None
        self.velocity = None
        self.database = StarDatabase()  # Add database to game
    
    def choose_mass(self):
        print(f"\nCoins: {self.coins}")
        print("\nChoose your star mass (affects lifespan and power):")

        print("1. Red Dwarf (0.3 M☉) - 20 coins")
        print("2. K-type Star (0.6 M☉) - 25 coins")
        print("3. G-type Star (1.0 M☉) - 35 coins")
        print("4. F-type Star (1.2 M☉) - 40 coins")
        print("5. A-type Star (1.8 M☉) - 45 coins")
        print("6. B-type Star (5.0 M☉) - 55 coins")
        print("7. Blue Giant (10.0 M☉) - 65 coins")
        print("8. Blue Supergiant (15.0 M☉) - 75 coins")

        choice = input("\nEnter choice (1, 2, 3, 4, 5, 6, 7, or 8): ")

        options = {
        "1": (0.3, 20, "Red Dwarf"),        
        "2": (0.6, 25, "K-type Star"),   
        "3": (1.0, 35, "G-type Star"),
        "4": (1.2, 40, "F-type Star"),
        "5": (1.8, 45, "A-type Star"),    
        "6": (5.0, 55, "B-type Star"), 
        "7": (10.0, 65, "Blue Giant"),
        "8": (15.0, 75, "Blue Supergiant")
        }
        
        if choice not in options:
            print("Invalid choice. Choose 1, 2, 3, 4, 5, 6, 7 or 8.")
            return self.choose_mass()

        mass, cost, mass_type = options[choice]

        if cost > self.coins:
            print(f"\nNot enough coins! You have {self.coins}, need {cost}.")
            return self.choose_mass()

        self.coins -= cost
        self.mass = mass
        
        print(f"\nYou chose a {mass_type} star with mass {mass} M☉!")
        print("\n" + "=" * 60)
        
        return mass
    
    def choose_luminosity(self):
        print(f"\nCoins remaining: {self.coins}")
        print("\nChoose luminosity (affects visibility and brightness):")
        
        # Luminosity options based on mass
        if self.mass < 0.7:
            # Dwarf range
            print("1. Very Low (5) - 5 coins")
            print("2. Low (15) - 10 coins")
        elif self.mass < 1.3:
            # Main Sequence range
            print("1. Normal (50) - 15 coins")
            print("2. Bright (80) - 25 coins")
        elif self.mass < 6:
            # Massive star range
            print("1. Bright (150) - 15 coins")
            print("2. Very Bright (300) - 25 coins")
        else:
            # Supermassive range
            print("1. Extremely Bright (500) - 15 coins")
            print("2. Ultra Luminous (1000) - 25 coins")

        choice = input("\nEnter choice (1 or 2):: ")
        
        if self.mass < 0.7:
            options = {"1": (5, 5), "2": (15, 10)}
        elif self.mass < 1.3:
            options = {"1": (50, 15), "2": (80, 25)}
        elif self.mass < 6:
            options = {"1": (150, 15), "2": (300, 25)}
        else:
            options = {"1": (500, 15), "2": (1000, 25)}

        if choice not in options:
            print("Invalid choice. Choose 1 or 2.")
            return self.choose_luminosity()

        luminosity, cost = options[choice]

        if cost > self.coins:
            print(f"\nNot enough coins! You have {self.coins}, need {cost}.")
            return self.choose_luminosity()

        self.coins -= cost
        self.luminosity = luminosity
        
        print(f"\nLuminosity set to {luminosity}!")
        print("\n" + "=" * 60)
        
        return luminosity
    
    def choose_velocity(self):
        print(f"\nCoins remaining: {self.coins}")
        print("\nChoose velocity (affects maneuverability and escape chances):")
        print("1. Slow (5 km/s) - 5 coins")
        print("2. Medium (15 km/s) - 10 coins")
        print("3. Fast (30 km/s) - 20 coins")
        print("4. Very Fast (60 km/s) - 35 coins")

        choice = input("\nEnter choice (1, 2, 3, or 4): ")
        
        options = {
            "1": (5, 5, "Slow"),
            "2": (15, 10, "Medium"),
            "3": (30, 20, "Fast"),
            "4": (60, 35, "Very Fast")
        }

        if choice not in options:
            print("Invalid choice. Choose 1, 2, 3, or 4.")
            return self.choose_velocity()

        velocity, cost, velocity_type = options[choice]

        if cost > self.coins:
            print(f"\nNot enough coins! You have {self.coins}, need {cost}.")
            return self.choose_velocity()

        self.coins -= cost
        self.velocity = velocity
        
        print(f"\nVelocity set to {velocity_type} ({velocity} km/s)!")
        print(f"\nFinal coins left: {self.coins}")
        print("\n" + "=" * 60)
        
        return velocity

    def build_star(self, star_name):
        mass = self.choose_mass()
        luminosity = self.choose_luminosity()
        velocity = self.choose_velocity()

        return Star(mass, luminosity, velocity, star_name)   # return new Star-class object with four parameters

        
    def play_stellar_encounter(self, star):
        """Encounter with a star from the database"""
        
        print("\n" + "=" * 60)
        print("A STAR APPROACHES!".center(60))
        print("=" * 60)

        # call back to class where we define the encountering star and create new object
        encounter = StellarEncounter(self.database)   
        attack_star = encounter.attack_star      # get data of the attack star
        
        print(f"\nYour star has encountered: {attack_star['name']}")
        print(f"Properties: {attack_star['mass']} M☉, {attack_star['luminosity']:.4f} L☉")
        print(f"Type: {attack_star['type']}")
        
        print("\n" + "─" * 60)
        print(f"How will {star.name} respond?")
        print("1. AGGRESSIVE - Try to dominate the encounter (risky but rewarding)")
        print("2. EVASIVE - Try to escape (safer, minimal changes)")
        print("3. BALANCED - Let your star's properties decide the outcome")
        
        choice = input("\nEnter choice (1, 2, or 3): ")

        # send these choices and the star to Encounter approach method and do the wanted approach
        survived, message, updated_star = encounter.encounter_approach(star, choice)
        
        print(message)

        # Return True if survived the encounter (return also updated player star), return false if didn't

        if survived:
            print("Updated star properties:")
            updated_star.star_summary()
            return True, updated_star

        else:
            return False, star
       

"""------------------------------------------- Main Game Loop -------------------------------------------------------"""
    
def play_game():
    game = Game()

    """ Naming """

    name = input("Give your star a name (or choose default by just pressing enter): ")

    if name == "":
        name = "Your Star"

    print(f"Your star is called {name}!")

    """ Game continued """
    star = game.build_star(name)
    star.star_description()
    star.draw()
    
    # Ask if player wants to continue to the encounter
    print("=" * 60)
    print(f"\n{star.name} is ready. Do you want to begin the cosmic journey?")
    print("1. Yes")
    print("2. No")
    choice = input("Enter choice (1 or 2): ")
    
    if choice != '1':
        print("\nThanks for creating your star! Come back when you're ready for adventure!")
        return
    
    # Play the stellar encounter -> loop
    survived, star = game.play_stellar_encounter(star)

    while survived:   # while survived is True
        print("=" * 60)
        print(f"\nCongratulations! {star.name} survived!")
        print("Want to test your chances against another star? \n1. Yes\n2. No\n")
        choice = input("Enter choice (1 or 2): ")

        if choice != '1':
            print(f"\nThanks for playing! {star.name} will continue drifting in space without your control!")
            print("\nFinal Star:")
            star.star_summary()
            star.draw()
            return
            
        survived, star = game.play_stellar_encounter(star)

    # when not survived (False) -> Game over
    print("=" * 60)
    print("\nGame Over! Would you like to create a new star and try again? \n1. Yes\n2. No\n")
    choice = input("Enter choice (1 or 2): ")

    if choice == '1':
        print("\n" + "=" * 60)
        print("STARTING NEW GAME...".center(60))
        print("=" * 60)
        play_game()

    else:
        print("\nThanks for playing! Better luck next time!")
        print("\nFinal Star:")
        star.star_summary()
        star.draw()
        return

play_game()


# In[ ]:





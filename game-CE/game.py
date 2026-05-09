#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:





# In[2]:


"""
Exoplanet Discovery Game

A game where you try to travel between exoplanets. You get points by visiting different planets,
but be careful as your tank runs empty fast travelling through the depths of space!!!

"""

import random


class Planet:
    """
    The exoplanets information that will be given:

    Attributes:
        name: Name of the planet
        distance: Distance from Earth in light-years
        radius: Radius relative to Earth
        discovery_year: Year the planet was discovered
    """

    def __init__(self, name, distance, radius, discovery_year):
        self.name = name
        self.distance = distance
        self.radius = radius
        self.discovery_year = discovery_year

    def info(self):
        """
        Providing information about the different exoplanets:
        
        """
        return (f"{self.name} | Distance: {self.distance} ly | "
                f"Radius: {self.radius} in Earth radii | "
                f"Discovered in the year: {self.discovery_year}")


class Player:
    """
    Useful information for the player in order to make your decision:

    Attributes:
        fuel: Shows how much fuel you have left
        score: Your score at the point you are now
    """

    def __init__(self):
        self.fuel = 1000.0 #you start with a fully filled tank
        self.score = 0 #you start with zero points

    def travel(self, planet):
        """
        Travel to a planet.

        The further the planet, the more fuel it will cost.
        The bigger the planet, the more points you get for reaching it.
        """
        fuel_cost = planet.distance * 0.5

        if fuel_cost > self.fuel:
            print("ERROR!!! CANNOT REACH DESTINATION, NOT ENOUGH FUEL. CHANGE DESTINATION!!!")
            return False

        self.fuel -= fuel_cost  #substracts fuel cost from your current fuel
        gained_score = int(planet.radius * 10) #amount of points you have earned
        self.score += gained_score  #add earned points to current score

        print(f" You have visited an exoplanet, welcome to: {planet.name}!")
        print(f"Remember, you lost some fuel. You used: {fuel_cost:.2f}")
        print(f"Congrats, you gained some points: {gained_score}")

        return True


class Game:
    """
   The game part
    """

    def __init__(self):
        self.player = Player()
        self.planets = self.load_planets()

    def load_planets(self):
        """
        Import the data about the exoplanets

        """
        return [
            Planet("Kepler-22b", 600, 2.4, 2011),
            Planet("Proxima Centauri b", 4.2, 1.3, 2016),
            Planet("TRAPPIST-1e", 39, 0.9, 2017),
            Planet("HD 209458 b", 159, 1.38, 1999),
            Planet("WASP-12b", 870, 1.9, 2008),
            Planet("K2-18 b", 124, 2.6, 2015),
            Planet("Kepler-62f", 1200, 1.41, 2013),
            Planet("Kepler-62e", 1200, 1.61, 2013),
            Planet("TOI-700 d", 101.4, 1.19, 2020),
            Planet("TOI-700 e", 101.4, 0.95, 2023),
            Planet("GJ 1214 b", 48, 2.85, 2009),
            ]

    def show_planets(self):
        #show your travel options
        print("\n Travel options:")
        for i, planet in enumerate(self.planets):  #number the planets
            print(f"{i + 1}. {planet.info()}")  #show number and corresponding planet info

    def play(self):
        """Play the game :)"""
        print("Welcome adventurer, be ready to travel through space!!!")
        print("Lets travel to as much exoplanets as possible and try and earn points!\n")

        while self.player.fuel > 0:
            print(f"\nFuel left: {self.player.fuel:.2f} | Score: {self.player.score}")
            
            
            #shuffels the list of planets each round to make sure you think about your choices
            random.shuffle(self.planets)
            self.show_planets()
            
            try:
                choice = int(input("Choose a planet (number) or 0 to return home safe: "))
            except ValueError:
                print("Invalid input!")
                continue

            if choice == 0:
                break

            if 1 <= choice <= len(self.planets):  #check if choice is possible
                planet = self.planets[choice - 1] #transform chose number to matching index
                self.player.travel(planet)  #deduct fuel, add score 
            else:
                print("Invalid choice! Number is out of the possible range")

        print("\n Welcome home!")
        print(f"Final Score: {self.player.score}")


if __name__ == "__main__":
    #create your game
    game = Game()
    #start the game
    game.play()


# In[ ]:





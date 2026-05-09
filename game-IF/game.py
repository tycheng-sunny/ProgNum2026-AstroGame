#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import random

#create a class for the stars
class Star:
    def __init__(self, name, constellation, magnitude, distance, spectral):
        self.name = name
        self.constellation = constellation
        self.magnitude = magnitude
        self.distance = distance
        self.spectral = spectral
#first hint: give constellation and distance
    def basic_hint(self):
        return f"Constellation: {self.constellation}\nDistance: {self.distance:.2f} ly"
#second hint, add magnitude and spectral type
    def full_hint(self):
        return (f"Constellation: {self.constellation}\n"
                f"Distance: {self.distance:.2f} ly\n"
                f"Magnitude: {self.magnitude:.2f}\n"
                f"Spectral type: {self.spectral}")
#open the star data
class StarDatabase:
    def __init__(self,df):
        self.df = pd.read_csv("hygdata_v42.csv.gz")
        # Filter stars with proper names
        self.df = self.df[self.df['proper'].notna()]
        self.used_indices = set()  #tracking stars

    def get_random_star(self):
        # Avoid repeats
        remaining = set(self.df.index) - self.used_indices
        if not remaining:
            self.used_indices.clear()
            remaining = set(self.df.index)
        idx = random.choice(list(remaining))
        self.used_indices.add(idx)
        row = self.df.loc[idx]
        #convert distance into ly
        distance_ly = row['dist'] * 3.262 if 'dist' in row else 0
        return Star(
            name=row['proper'],
            constellation=row['con'] if 'con' in row and row['con'] else "Unknown",
            magnitude=row['mag'] if 'mag' in row else 0,
            distance=distance_ly,
            spectral=row['spect'] if 'spect' in row and row['spect'] else "Unknown"
        )
#define class for players
class Player:
    def __init__(self, name):
        self.name = name   #players name
        self.score = 0
        self.lives = 5     #number of lives
#add points
    def add_score(self, points):
        self.score += points
#lose a life
    def lose_life(self):
        self.lives -= 1
#class for game
class StarExplorer:
    def __init__(self, db, rounds=5):
        self.db = db
        self.rounds = rounds
#main game loop
    def start(self):
        #prints instructions
        print("Welcome to Star Explorer Challenge!")
        print("The goal of this game is to guess the correct star, based on the hints given.")
        print("If you guess wrong the first time, you get more hints. You have 5 lives total. Good luck!")
        pname = input("Enter your name: ").strip()  #input your name
        player = Player(pname)

        for i in range(1, self.rounds + 1): #loops the rounds
            print(f"\n--- Round {i} ---")  #prints the rounds
            star = self.db.get_random_star()  #gives a random star
            tries = 2

            while tries > 0:
                if tries == 2:
                    print(star.basic_hint())  #print first hint
                else:
                    print("Extra hint:")
                    print(star.full_hint())   #print advanced hint

                guess = input("Guess the star's name: ").strip()  #input guess
                if guess.lower() == star.name.lower():
                    points = 10 if tries == 2 else 5              #for basic hint, 10 points, for advanced hint 5 points
                    print(f"Correct! You earn {points} points.")
                    player.add_score(points)
                    break
                else:
                    tries -= 1
                    player.lose_life()  #lose life
                    if tries > 0:
                        print(f"Incorrect! Try again. Lives left: {player.lives}") #for 1 hint
                    else:
                        print(f"Incorrect! The correct answer was: {star.name}")   #if not guessed
                        print(f"Lives left: {player.lives}")
                if player.lives == 0:  #if no lives left
                    print("\nGame Over! You lost all your lives.")
                    print(f"Final Score: {player.score}")
                    return

        print("Congratulations! You explored all stars.")
        print(f"Final Score: {player.score}")


if __name__ == "__main__":   #loads database, create game objects and starts the game
    db = StarDatabase("hygdata_v42.csv.gz")
    game = StarExplorer(db, rounds=5)
    game.start()


# In[ ]:





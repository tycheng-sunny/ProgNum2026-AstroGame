#!/usr/bin/env python
# coding: utf-8

# In[2]:


import time

class Planet:
    def __init__(self, name, gravity, distance, energy, event="None"):
        self.name = name
        self.gravity = gravity
        self.distance = distance
        self.energy = energy
        self.event = event
      


class Game:
    def __init__(self):
        self.planets = [
            Planet("Mercury", 3.70, 0.39, 9116, "Victory"),
            Planet("Venus", 8.87, 0.72, 2611, "None"),
            Planet("Earth", 9.81, 1.00, 1361, "Medicine"),
            Planet("Mars", 3.71, 1.52, 589, "None"),
            Planet("Jupiter", 24.79, 5.20, 50.5, "Alien"),
            Planet("Saturn", 10.44, 9.58, 15, "None"),
            Planet("Uranus", 8.87, 19.20, 3.7, "None"),
            Planet("Neptune", 11.15, 30.05, 1.5, "None"),
            Planet("Pluto", 0.62, 39.5, 1.0, "None")
        ]

        self.current_index = 8
        self.days_left = 0
        self.electricity = 0
        self.food = 0
        self.unlocked_foods = ["Pasta", "Quiche", "Viande"]
        self.game_over = False

    def travel_cost(self, p1, p2):
        return int(abs(p1.distance - p2.distance))*2

    def produce_electricity(self):
        planet = self.planets[self.current_index]
        generated = planet.energy * 10
        self.electricity += generated
        print(f"Produced {generated:.2f} electricity on {planet.name}.")
        time.sleep(2)

    def check_event(self):
        planet = self.planets[self.current_index]

        if planet.event == "None":
            print(f"Not much to do on {planet.name}...")
            return False

        elif planet.event == "Medicine":
            print("Earth Event")
            self.produce_electricity()
            self.days_left += 1
            print("You gathered medicine.")
            planet.event = "None"
            return True

        elif planet.event == "Victory":  
            print("You won!")
            self.game_over = True
            return True 

        elif planet.event == "Alien":
            print("Alien Event")
            choice = input("Spend the day with alien? (y/n): ")

            if choice == "y":
                print("You learned Alien Soup!")
                if "Alien Soup" not in self.unlocked_foods:
                    self.unlocked_foods.append("Alien Soup")
                self.days_left += 1

            planet.event = "None"
            return True



    def travel(self):
        direction = input("Go (f)orth or (b)ack? ")

        if direction == "f":
            new_index = self.current_index - 1
        elif direction == "b":
            new_index = self.current_index + 1
        else:
            print("Invalid direction!")
            return

        if new_index < 0:
            print("You got burned in the Sun!")
            exit()

        if new_index >= len(self.planets):
            print("Edge of space!")
            return

        cost = self.travel_cost(
            self.planets[self.current_index],
            self.planets[new_index]
        )

        print(f"Travel cost: {cost}")

        if self.electricity < cost:
            print("Not enough electricity!")
            return

        self.electricity -= cost
        self.current_index = new_index
        print(f"Moved to {self.planets[self.current_index].name}")

    def stay(self):
        self.food -= 5
        self.produce_electricity()
        print("Stayed on planet.")

    def cook(self):
        choice = input("Produce food? (y/n): ")

        if choice != "y":
            return

        print("Available:", self.unlocked_foods)
        food_type = input("Choose food: ")

        if food_type == "Pasta":
            self.electricity -= 10
            self.food += 5

        elif food_type == "Quiche":
            self.electricity -= 15
            self.food += 7.5

        elif food_type == "Viande":
            self.electricity -= 20
            self.food += 10

        elif food_type == "Alien Soup" and "Alien Soup" in self.unlocked_foods:
            self.electricity -= 10
            self.food += 12

        else:
            print("Unknown recipe!")

    def setup(self):
        name = input("Your name: ")

        print(f"{name}, mission start...")
        answer = input("Accept mission? Yes/No: ")
        if answer == "Yes" :
            print('Let\'s go!')
        
        if answer == "No":
            print("Too bad, you're going anyway.")

        mode = input("Mode (easy/normal/hard): ")

        if mode == "easy":
            self.electricity = 100
            self.food = 60
        elif mode == "normal":
            self.electricity = 70
            self.food = 40
        else:
            self.electricity = 50
            self.food = 25

    def play(self):
        self.setup()

        while self.days_left < 12 and self.food > 0 and self.electricity > 0 and not self.game_over:

            planet = self.planets[self.current_index]

            if self.check_event():
                continue

            print(f"\nDay {self.days_left}")
            print(f"Planet: {planet.name}")
            print(f"Food: {self.food}")
            print(f"Electricity: {self.electricity:.2f}")

            action = input("(t)ravel or (s)tay: ")

            if action == "t":
                self.travel()
            else:
                self.stay()

            self.cook()

            # Daily consumption
            self.food -= 7
            self.days_left += 1

            if self.food < 10:
                print("Food running low!")

            if self.electricity < 20:
                print("Electricity running low!")

        self.end_game()

    def end_game(self):
        if self.game_over:
            print("Mission successful! You delivered the medicine! 🚀")
        elif self.days_left >= 12:
            print("You lost: ran out of time.")
        elif self.food <= 0:
            print("You starved.")
        elif self.electricity <= 0:
            print("Out of electricity.")

    print("Thanks for playing!")

game = Game()
game.play()


# In[ ]:





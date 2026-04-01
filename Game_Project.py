#!/usr/bin/env python
# coding: utf-8

# In[18]:


print(" Welcome to your first space journey! (and possibly you last...)")
class Planet:
    def __init__(self, name, distance, temperature, planet_type, danger):
        """ This function initialises the class. Name will provide the name of the planet.
        Distance will give the distance from Earth to the planet. Temperature will provide the temperature on the planet.
        Planet_type will provide the type of planet you landed on. Danger will provide a score, from 1 to 10, showing how dangerous the planet is.
        Higher danger score will make life on the planet more difficult. Values are for large proportions taken from the NASA Exoplanet Archive.
        Values like danger and type are based on temperature mostly, or other known properties of the planet that would form a bigger danger.
        Type will be largely fictional, to add some diversity."""
        self.name = name
        self.distance = distance
        self.temperature = temperature
        self.type = planet_type
        self.danger = danger

    def description(self):
        """ This function will show you in a quick list, what the properties of your chosen planet are."""
        desc = f" Planet: {self.name} \n Distance: {self.distance} lightyears \n Surface Temperature: {self.temperature} K \n Planet type: {self.type} \n Danger: {self.danger}"
        return desc

    def events(self):
        """This function will contain things that will happen once you have reached the planet."""
        planet_events = {
            'Kepler-186e': {
                'a': ('Go back to Earth.', 'That was rather pointless... GAME OVER!'),
                'b': ('Go outside and head to the left.', 'You find a goat! Go pet it!',
                {
                    'a' : ('Pet the goat', 'The goat enjoyes it, you bring the goat home and are forever remembered for bring the first alien to Earth. YOU WIN!'),
                    'b': ('Run away from the goat', 'The goat sees you as a threat. It chases you and the goat attacks you. GAME OVER!')
                }
                 ),
                'c': ('Go outside and head to the right.', 'You fall off a cliff you did not see. GAME OVER!')
            },
            'Proxima Centauri B': {
                'a': ('Go back to Earth.', 'That was rather pointless... GAME OVER!'),
                'b': ('Go outside and head to the left.', 'You freeze to death. GAME OVER!'),
                'c': ('Go outside and head to the right.', 'You burn to death. GAME OVER!')
            },
            'Teegarden star B': {
                'a': ('Go back to Earth.', 'That was rather pointless... GAME OVER'),
                'b': ('Go outside and head to the left.', 'You go into a beautiful jungle and see a feline animal. ',
                {
                    'a' : ('Approach it and pet it.', 'This was not just any house cat, it tears you apart. GAME OVER!'),
                    'b' : ('Take a picture of the feline and leave.', 'You return home with proof of alien life. YOU WIN!'),
                    'c' : ('Try to hunt it, you have to eat after all...', 'Turns out, the feline has to eat as well... GAME OVER!')
                }
                     ),
                'c': ('Go outside and head to the right.', 'You are attacked by an alien and die. GAME OVER!')
            },
            'TOI-1452 b': {
                'a': ('Go back to Earth.','That was rather pointless... GAME OVER!'),
                'b': ('Go outside and head to the left.', 'You are met by a strange creature, an octopus-like animal but it has ten tentacles and hands on them.',
                {
                    'a' : ('Take out your harpoon and turn it into sushi.', 'You return to Earth with extremely rare sushi and make a lot of money! YOU WIN!'),
                    'b' : ('Move closer and inspect it', 'It turns out the creature is very strong, it uses it hands to rip your helmet of and you drown! GAME OVER!')
                }
                     ),
                'c': ('Go outside and head to the right.', 'You come across an alien killer whale who sees you as its next meal. GAME OVER!')
            },
        }
        return planet_events.get(self.name, {})

kepler_186e = Planet(
    name = 'Kepler-186e',
    distance = 580,
    temperature = 319,
    planet_type = 'Rocky',
    danger = 1
)
Proxima_Centauri_B = Planet(
    name = 'Proxima Centauri B',
    distance = 4.25,
    temperature = 216,
    planet_type = 'Rocky',
    danger = 7
)
teegarden_b = Planet(
    name = 'Teegarden star B',
    distance = 12.49,
    temperature = 280,
    planet_type = 'Rocky',
    danger = 3
)
toi_1452= Planet(
    name = 'TOI-1452 b',
    distance = 12.49,
    temperature = 315,
    planet_type = 'Oceanic',
    danger = 4
)
planets = [kepler_186e, Proxima_Centauri_B, teegarden_b, toi_1452]
letters = ['a', 'b', 'c', 'd']
for letter, planet in zip(letters,planets):
    print(f"{letter})",planet.description())
destination = input("Enter the letter of the planet you want to travel to: ")
if destination in letters:
    index = letters.index(destination)
    chosen_planet = planets[index]
    print(f" Your journey begins to:")
    print(chosen_planet.description())
else :
    print("No planet chosen.")


actions = chosen_planet.events()
for letter, action in actions.items():
    print(f"{letter}) {action[0]}")

choice = input("Enter your choice: ")

if choice in actions:
    first_choice = actions[choice]
    print("\n" + first_choice[1])

    if len(first_choice) > 2:
        second_actions = first_choice[2]

        # The second set of choices will be shown.
        for letter, action in second_actions.items():
            print(f"{letter}) {action[0]}")

        choice2 = input("Enter your next choice: ")

        if choice2 in second_actions:
            print("\n" + second_actions[choice2][1])
        else:
            print("Nothing happens")
else:
    print("Nothing happens")


# In[ ]:





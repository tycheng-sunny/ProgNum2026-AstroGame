import random 

# CLASSES

class Planet:
    """Represents a planet in the Solar System."""
    def __init__(self, name, distance, gravity, diameter):
        # Initialize planet properties
        self.name = name
        self.distance = distance  # Distance from the Sun in million km
        self.gravity = gravity    # Gravity relative to Earth (1g)
        self.diameter = diameter  # Diameter in km

    def info(self):
        """Return a formatted string with planet information."""
        return f"{self.name}: Distance {self.distance}M km | Gravity {self.gravity}g | Diameter {self.diameter} km"

class Question:
    """Represents an astronomy quiz question."""
    def __init__(self, prompt, options, answer):
        # prompt: question text
        # options: list of answer choices
        # answer: index of correct choice (0-based)
        self.prompt = prompt
        self.options = options
        self.answer = answer

    def ask(self):
        """Ask the player the question and return True if correct, False otherwise."""
        print("\nQUIZ TIME!")
        print(self.prompt)
        for idx, opt in enumerate(self.options):
            # Display options with numbers starting from 1
            print(f"{idx+1}. {opt}")
        choice = input(f"Your answer (1-{len(self.options)}): ").strip()
        # Validate input
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(self.options):
            print("Invalid choice! Counting as wrong.")
            return False
        # Check if player's choice matches the correct answer
        return int(choice) - 1 == self.answer

class Player:
    """Represents the player (spaceship captain)."""
    def __init__(self, name):
        self.name = name
        self.fuel = 0  # Starts with zero fuel
        self.score = 0  # Player score
        self.current_planet_idx = 0  # Index of current planet (starts at Mercury)
        self.wrong_answers = 0  # Count of wrong answers (3 strikes = game over)

    def gain_fuel(self, fuel_amount):
        """Increase fuel by a given amount."""
        self.fuel += fuel_amount
        print(f"You gained {fuel_amount} fuel! Current fuel: {self.fuel}")

    def update_score(self, correct, score_reward=10):
        """Update score and wrong answer count based on correctness."""
        if correct:
            self.score += score_reward
            print(f"Correct! +{score_reward} points. Total score: {self.score}")
        else:
            self.wrong_answers += 1
            print(f"Wrong answer! Strike {self.wrong_answers}/3. No fuel gained!")

    def status(self, planet_name):
        """Print current player status."""
        print(f"\nCurrent Planet: {planet_name} | Score: {self.score} | Fuel: {self.fuel} | Strikes: {self.wrong_answers}/3")

# GAME LOGIC

class PlanetHopperChallenge:
    """Main game class for the Planet Hopper Challenge."""
    def __init__(self, player_name):
        # Initialize player
        self.player = Player(player_name)

        # Initialize planets in linear order from Mercury to Neptune
        self.planets = [
            Planet("Mercury", 57.9, 0.38, 4880),
            Planet("Venus", 108.2, 0.91, 12104),
            Planet("Earth", 149.6, 1.0, 12756),
            Planet("Mars", 227.9, 0.38, 6792),
            Planet("Jupiter", 778.5, 2.34, 142984),
            Planet("Saturn", 1433.5, 1.06, 120536),
            Planet("Uranus", 2872.5, 0.92, 51118),
            Planet("Neptune", 4495.1, 1.19, 49528)
        ]

        # Initialize a large quiz question bank
        self.questions = [
            Question("Which planet is known as the Red Planet?", ["Venus", "Mercury", "Mars", "Jupiter"], 2),
            Question("Which galaxy is closest to the Milky Way?", ["Triangulum", "Andromeda", "Messier 87", "Whirlpool"], 1),
            Question("How long does Earth take to orbit the Sun?", ["30 days", "100 days", "365 days", "687 days"], 2),
            Question("Which comet has an orbital period of ~76 years?", ["Hale-Bopp", "Encke", "Swift-Tuttle", "Halley"], 3),
            Question("Which planet has the strongest gravity?", ["Neptune", "Saturn", "Jupiter", "Earth"], 2),
            Question("Which planet is known for its rings?", ["Saturn", "Uranus", "Jupiter", "Neptune"], 0),
            Question("Which planet has the hottest surface?", ["Venus", "Mercury", "Mars", "Earth"], 0),
            Question("Which planet is the largest in our solar system?", ["Earth", "Saturn", "Jupiter", "Uranus"], 2),
            Question("Which planet spins on its side?", ["Neptune", "Uranus", "Mars", "Venus"], 1),
            Question("Which is the smallest planet in the Solar System?", ["Mercury", "Mars", "Venus", "Earth"], 0),
            Question("Which planet has the fastest orbit around the Sun?", ["Mars", "Venus", "Earth", "Mercury"], 3),
            Question("Which planet is known as the Morning Star?", ["Venus", "Mars", "Jupiter", "Mercury"], 0),
            Question("Which dwarf planet is located in the asteroid belt?", ["Eris", "Pluto", "Ceres", "Haumea"], 2),
            Question("Which planet is furthest from the Sun?", ["Uranus", "Neptune", "Saturn", "Jupiter"], 1),
            Question("Which planet is known as the Evening Star?", ["Jupiter", "Mars", "Mercury", "Venus"], 3),
            Question("Which planet has a day longer than its year?", ["Venus", "Mercury", "Mars", "Earth"], 0),
            Question("Which planet has the Great Red Spot?", ["Jupiter", "Saturn", "Neptune", "Earth"], 0),
            Question("Which planet has the most moons?", ["Jupiter", "Saturn", "Mars", "Uranus"], 1),
            Question("Which planet is nicknamed the Ice Giant?", ["Neptune", "Uranus", "Saturn", "Jupiter"], 0),
            Question("Which planet is known for its blue color due to methane?", ["Uranus", "Earth", "Neptune", "Saturn"], 2)
        ]

    def fuel_needed(self, current_idx, next_idx):
        """
        Calculate fuel needed to jump to next planet.
        Formula: distance difference / 10 * average gravity between planets.
        """
        current = self.planets[current_idx]
        next_p = self.planets[next_idx]
        avg_gravity = (current.gravity + next_p.gravity) / 2
        return int(abs(next_p.distance - current.distance) / 10 * avg_gravity)

    def start(self):
        """Start the main game loop."""
        # Introduction
        print(f"Welcome, Captain {self.player.name}, to Planet Hopper Challenge!")
        print(f"You have been asked to go on a journey, but not just any journey. You're gonna be the first astronaut ever to fly to each planet.")
        print("But there is a problem. You started on Mercury but now have ZERO fuel left.")
        print("On each planet you will be asked a question, answer correctly to gain fuel and jump to the next planet.")
        print("But be careful! Three wrong answers and your spaceship explodes!\n")

        # Main game loop
        while self.player.current_planet_idx < len(self.planets) - 1:
            # Check if player reached 3 strikes
            if self.player.wrong_answers >= 3:
                print("\nYour spaceship sustained too much damage from repeated meteors!")
                print("The engines fail and your ship explodes into space...")
                print("GAME OVER.")
                return  # End game

            current_idx = self.player.current_planet_idx
            next_idx = current_idx + 1
            current_planet = self.planets[current_idx]
            next_planet = self.planets[next_idx]

            # Show player status
            self.player.status(current_planet.name)

            # Randomly select a question for the current planet
            question = random.choice(self.questions)
            correct = question.ask()

            if correct:
                # Player answered correctly: gain fuel and score
                fuel_for_jump = self.fuel_needed(current_idx, next_idx)
                self.player.gain_fuel(fuel_for_jump)
                self.player.update_score(correct)

                # Jump to next planet
                print(f"\nJumping from {current_planet.name} to {next_planet.name}!")
                self.player.fuel -= self.fuel_needed(current_idx, next_idx)
                self.player.current_planet_idx = next_idx
            else:
                # Player answered incorrectly: story event and possible pushback
                self.player.update_score(correct)
                if self.player.current_planet_idx > 0:
                    # Push back to previous planet
                    prev_planet = self.planets[self.player.current_planet_idx - 1]
                    print(f"\nOh no! When you were trying to jump to the next planet it failed, since you didn't have enough fuel.")
                    print(f"You were drifting in space when you suddenly hear a giant bang. You werehit by a METEOR!!!")
                    print(f"Your ship sustained some damage, but it still works, but you have been pushed back to {prev_planet.name}.")
                    self.player.current_planet_idx -= 1
                else:
                    # If on Mercury, can't go back further
                    print("\nYou remain on Mercury. Try the question again.")

        # Player reaches Neptune
        print("\nCongratulations! You reached Neptune!")
        self.player.status("Neptune")
        print("Mission Complete!")
        print(f"Great job captain, you did the unthinkable. You should have enough fuel to jump back to Earth.")
        print(f"YOU WIN")


if __name__ == "__main__":
    # Ask for player name
    name = input("Enter your name, Captain: ").strip()
    # Create game instance
    game = PlanetHopperChallenge(name)
    # Start the game
    game.start()
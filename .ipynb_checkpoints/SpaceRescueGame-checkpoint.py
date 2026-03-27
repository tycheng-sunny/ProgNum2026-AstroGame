import numpy as np
import time
import sys

def type_print(text, speed = 0.03):
    # Print everything like someones typing
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

class Planet:
    """ A planet with astronomical data
    """

    def __init__(self, name, distance_au, gravity, temperature, moons, points_value):
        """
        Create a planet.

        Parameters:
        name:
            Name of the planet
        distance_au:
            Distance from the Sun in astronomical units
        gravity:
            Relative to Earth
        temperature:
            Average temperature in degrees Celsius
        moons:
            Number of moons
        points:
            Points gained when exploring the planet
        """
        self.name = name
        self.distance_au = distance_au
        self.gravity = gravity
        self.temperature = temperature
        self.moons = moons
        self.points_value = points_value

    def description(self):
        """Return a short description of the planet
        """
        return (
            f"{self.name}: distance = {self.distance_au} AU, "
            f"gravity = {self.gravity} g, "
            f"temperature = {self.temperature} °C, "
            f"moons = {self.moons}"
        )

class Ship:
    """Represent the player's spaceship
    """

    def __init__(self, fuel = 120, health = 100):
        """
        Create the ship

        Parameters:
        fuel:
            Starting fuel
        health:
            Starting ship health
        """
        self.fuel = fuel
        self.health = health
        self.points = 0
        self.rescues = 0
        self.current_planet = "Earth"

    def is_destroyed(self):
        """Return True if the ship can no longer continue and is destroyed
        """
        return self.health <= 0 or self.fuel <= 0

    def status(self):
        """Return the status of the ship
        """
        return (
            f"Ship status -> Fuel: {self.fuel}, "
            f"Health: {self.health}, "
            f"Points: {self.points}, "
            f"Rescues: {self.rescues}, "
            f"Location: {self.current_planet}"
        )

class SpaceRescueGame:
    """Main game
    """

    def __init__(self):
        """Create the game, planets, ship, and mission targets
        """
        self.planets = self.load_planets()
        self.ship = Ship()
        self.turns = 0
        self.max_turns = 10
        self.target_rescues = 3
        self.visited = set(["Earth"])

    def load_planets(self):
        """Create the planet list with astronomical data
        """
        return [
            Planet("Mercury", 0.39, 0.38, 167, 0, 8),
            Planet("Venus", 0.72, 0.90, 464, 0, 10),
            Planet("Earth", 1.00, 1.00, 15, 1, 5),
            Planet("Mars", 1.52, 0.38, -65, 2, 15),
            Planet("Jupiter", 5.20, 2.53, -110, 95, 25),
            Planet("Saturn", 9.58, 1.07, -140, 146, 30),
            Planet("Uranus", 19.22, 0.89, -195, 27, 35),
            Planet("Neptune", 30.05, 1.14, -200, 14, 40),
        ]
        
    def list_planets(self):
        """Print all planets except the current one
        """
        type_print("\nAvailable destinations:")
        for i, planet in enumerate(self.planets, start = 1):
            if planet.name != self.ship.current_planet:
                type_print(f"{i}. {planet.description()}")

    def get_planet_by_choice(self, choice):
        """Convert a number choice into a planet object
        """
        if 1 <= choice <= len(self.planets):
            return self.planets[choice - 1]
        return None

    def travel_cost(self, planet):
        """Calculate fuel cost to travel.
            Uses difference in distance as the cost
        """
        current = self.get_current_planet()
        distance_difference = abs(planet.distance_au - current.distance_au)
        return int(distance_difference * 3) + 5

    def get_current_planet(self):
        """Return the current planet object
        """
        for planet in self.planets:
            if planet.name == self.ship.current_planet:
                return planet
        raise ValueError("Planet not found")
        
    def travel_to_planet(self, planet):
        """Make trip to planet
        """
        cost = self.travel_cost(planet)

        type_print(f"\nTravelling from {self.ship.current_planet} to {planet.name}...")
        type_print(f"Fuel cost: {cost}")

        if self.ship.fuel < cost:
            type_print("Not enough fuel for this trip, choose another destination.")
            return False

        self.ship.fuel -= cost
        self.ship.current_planet = planet.name
        self.visited.add(planet.name)
        self.turns += 1

        type_print(f"Arrived at {planet.name}.")
        return True

    def apply_planet_effects(self, planet):
        """Apply gameplay effects based on astronomy data
        """
        type_print("\nPlanet effects:")

        # Temperature hazard
        
        if planet.temperature > 200:
            type_print("Extreme heat damages your ship. Health -15")
            self.ship.health -= 15
        elif planet.temperature < -150:
            type_print("Extreme cold damagas your ship. Health -10")
            self.ship.health -= 10
        else:
            type_print("Temperature is manageable.")

        # Gravity hazard
        
        if planet.gravity > 2.0:
            type_print("High gravity makes landing difficult.")
            self.ship.health -= 10
        elif planet.gravity < 0.5:
            type_print("Low gravity makes landing is easy.")
        else:
            type_print("Gravity is moderate.")

        # Reward
        
        type_print(f"You collect {planet.points_value} points.")
        self.ship.points += planet.points_value

    def rescue_event(self, planet):
        """Determine whether there is an astronaut on the planet.
            The chance is higher on planets with moons, because planets with moons are interesting.
        """
        base_chance = 0.30
        moon_bonus = min(planet.moons / 200, 0.35)
        chance = base_chance + moon_bonus

        if np.random.random() < chance:
            type_print("You found and rescued an astronaut!")
            self.ship.rescues += 1
        else:
            type_print("No astronauts found on this planet.")

    def random_event(self):
        """Trigger a random event after travel
        """
        type_print("\nRandom event:")

        event = np.random.choice(["none", "solar_storm", "fuel_cache", "meteor_shower", "repair_drones"])

        if event == "none":
            type_print("Space is quiet. Nothing unusual happens.")
        elif event == "solar_storm":
            type_print("A solar storm hits the ship. Health -12.")
            self.ship.health -= 12
        elif event == "fuel_cache":
            type_print("You discover an abandoned fuel cache. Fuel +15.")
            self.ship.fuel += 15
        elif event == "meteor_shower":
            type_print("A meteor shower strikes the ship. Health -10.")
            self.ship.health -= 10
        elif event == "repair_drones":
            type_print("Friendly repair drones help you. Health +10.")
            self.ship.health = min(100, self.ship.health + 10)

    def choose_destination(self):
        """Ask the player where to travel
        """
        self.list_planets()

        while True:
            try:
                choice = int(input("\nChoose a planet number to travel to: "))
                planet = self.get_planet_by_choice(choice)

                if planet is None:
                    type_print("Invalid number. Try again.")
                elif planet.name == self.ship.current_planet:
                    type_print("You are already there. Choose another planet.")
                else:
                    return planet
            except ValueError:
                type_print("Please type a valid number.")

    def check_win(self):
        """Check if player has won
        """
        return self.ship.rescues >= self.target_rescues
    
    def check_loss(self):
        """Check if player has lost
        """
        return self.ship.is_destroyed() or self.turns >= self.max_turns

    def show_end_message(self):
        """Print the end-of-game message
        """
        type_print("\n==========================================")
        if self.check_win():
            type_print("\nMission accomplished! Your rescue mission was successful.")
        elif self.check_loss():
            type_print("\nMission failed. All astronauts you haven't rescued will die.")
        type_print("==========================================")
        type_print(self.ship.status())
        type_print(f"Visited planets: {sorted(self.visited)}")

    def run_turn(self):
        """Run one game turn
        """
        type_print(self.ship.status())
        destination = self.choose_destination()

        travelled = self.travel_to_planet(destination)
        if not travelled:
            return

        self.apply_planet_effects(destination)
        self.rescue_event(destination)
        self.random_event()

    def run(self):
        """Run the full game loop
        """
        
        type_print("==========================================")
        type_print("🚀 Welcome to SPACE RESCUE 🚀")
        type_print("==========================================")
        type_print("You are the captain of a rescue ship.")
        type_print("Astronauts are stranded across the Solar System.")
        type_print("Travel to planets, and rescue them, but watch out for your health and fuel, if they run out, you lose!")
        type_print("\nWin condition:")
        type_print(f"- Rescue at least {self.target_rescues} astronauts")
        type_print(f"- Survive for up to {self.max_turns} turns\n")

        while not self.check_win() and not self.check_loss():
            self.run_turn()

            if self.ship.health <= 0:
                type_print("\nYour ship has been destroyed.")
            elif self.ship.fuel <= 0:
                type_print("\nYou ran out of fuel.")
            elif self.turns >= self.max_turns:
                type_print("\nYou ran out of mission time.")

        self.show_end_message()

if __name__ == "__main__":
    SpaceRescueGame().run()
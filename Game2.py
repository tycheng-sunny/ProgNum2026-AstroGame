#!/usr/bin/env python
# coding: utf-8

# ### Game: Alien invasion... ### 

# Destroying their home before they destroy us...

# In[6]:


print(f" PROLOGUE")
print(f" Alien 1: ksfjowkj sdflpe oiod!")
print(f" Translation: Humans are awful!")
print(f" Alien 2: asldkf weio iosj fj!")
print(f" Translation: We should destroy them!")
print(f" Alien 1: asd wioio sloes pjfle aienfi...")
print(f" Translation: But first, we have to find their home...")
print()


# In[8]:


print(f" THE PRESENT")
print(f" Agent: We have a HUGE problem... It has reached our ears that aliens are planning to destroy Earth. But the worst thing is, we have no way to stop them. Therefore, we have to find their home first and eliminate the threat they pose.")
print(f" Agent: It is YOUR task to find it. Do it fast, or they'll find us...")
print()


# In[19]:


from astroquery.gaia import Gaia
import astropy.units as u
from IPython.display import display, Math  # Only needed for Jupyter
import random


class Gaiaquery:  # quering the data from Gaia
    def __init__(self, limit=50, max_distance_pc=10):  # i want 50 stars within 10 pc
        self.limit = limit
        self.max_distance_pc = max_distance_pc

    def query_nearby_stars(self):
        query = f"""
        SELECT TOP {self.limit}
            source_id,
            ra, dec,
            parallax,
            phot_g_mean_mag,
            teff_gspphot
        FROM gaiadr3.gaia_source
        WHERE parallax >= {1000/self.max_distance_pc}
        AND parallax IS NOT NULL
        ORDER BY parallax DESC
        """

        job = Gaia.launch_job(query)
        results = job.get_results()
        return results


class Star:
    def __init__(self, source_id, ra, dec, parallax, magnitude, temperature):
        self.source_id = source_id
        self.ra = ra
        self.dec = dec
        self.parallax = parallax
        self.magnitude = magnitude
        self.distance = self.compute_distance()
        self.temperature = temperature
        self.spectral_type = self.get_spectral_type()

    def compute_distance(self):
        return 1000 / self.parallax if self.parallax else None

    def __repr__(self):
        if self.distance is None:
            return f"Star(id={self.source_id}, dist=Unknown)"
        return f"Star(id={self.source_id}, dist={self.distance:.2f} pc)"

    def get_spectral_type(self):
        t = self.temperature
        if t is None:
            return None
        elif t > 30000:
            return "O"
        elif t > 10000:
            return "B"
        elif t > 7500:
            return "A"
        elif t > 6000:
            return "F"
        elif t > 5200:
            return "G"
        elif t > 3700:
            return "K"
        else:
            return "M"


class StarFactory:
    @staticmethod
    def from_gaia_table(table):
        stars = []
        for row in table:
            star = Star(
                source_id=row['SOURCE_ID'],
                ra=row['ra'],
                dec=row['dec'],
                parallax=row['parallax'],
                magnitude=row['phot_g_mean_mag'],
                temperature=row['teff_gspphot']
            )
            stars.append(star)
        return stars


gaia_service = Gaiaquery(limit=50, max_distance_pc=10)

results = gaia_service.query_nearby_stars()

stars = StarFactory.from_gaia_table(results)


class SpectralTypePuzzle:
    """The first puzzle where they have to input the right spectral type. This code
    checks if it is right"""

    def __init__(self):
        # Pick the "correct" spectral type for the puzzle
        # Here we choose the coldest type (M) for the example
        self.target_type = "K"

    def play(self, stars):
        while True:
            print("\nAgent: We know that they live around the second coldest type of star...")
            user_type = input("Enter the spectral type of the target star: ").strip().upper()

            filtered = [s for s in stars if s.spectral_type == user_type]

            if user_type == self.target_type:
                print("\nAgent: Great work! We're one step closer to finding those evil creatures...")
                print(f"Agent: There are {len(filtered)} stars of spectral type {user_type}.")
                print("The resulting stars:")
                for star in filtered:
                    print(star)
                return filtered  # exit loop and return correct stars
            else:
                print("\nAlien 1: oijeoijeoije dkwj wpdfhs jf!")
                print("Translation: Hahaha, stupid humans!")
                print("Agent: Try again, and hopefully this time you won't make stupid mistakes...")


class MathPuzzle:
    """The second puzzle, they have to solve the maths equation. This checks if its right and gives the right star"""

    def __init__(self, stars, target_index, equation_text):
        """
        stars: list of remaining stars
        target_index: index of the correct star in stars list (0-based)
        equation_text: LaTeX equation string to display
        """
        self.stars = stars
        self.target_index = target_index
        self.equation_text = equation_text

    def play(self):
        print("\nAgent: To find the correct star, solve this equation first...")

        # Display equation nicely if in Jupyter
        try:
            display(Math(self.equation_text))
        except NameError:
            # fallback for console: print raw LaTeX
            print(self.equation_text)

        while True:
            try:
                user_input = int(input(f"Enter the index of the correct star: "))
                if user_input == self.target_index:
                    print("\nAgent: Correct! We've pinpointed the alien star!")
                    print(f"The star is: {self.stars[user_input]}")
                    return self.stars[user_input]
                else:
                    print("\nAlien 1: oisdn! Sdlkfkw jjojw lkdsfow lkjl!")
                    print("Translation: Wrong! Hahaha, humans keep failing!")
                    print("Agent: Argh!")
                    print("Agent: We think this number has something to do with the star id...")
                    print("Keep in mind that the index goes from 0 to 4.")
            except ValueError:
                print(f"Please enter a number between 0 and {len(self.stars)-1}.")


def scramble(word):
    letters = list(word.replace(" ", "").upper())
    while True:
        random.shuffle(letters)
        scrambled = ''.join(letters)
        if scrambled != word.replace(" ", "").upper():
            return scrambled


class PlanetAnagramPuzzle:
    """The third and final puzzle, makes an anagram they have to solve"""

    def __init__(self, correct_planet, decoy_planets):
        """
        correct_planet: string
        decoy_planets: list of strings
        """
        self.correct_planet = correct_planet.upper()
        self.all_planets = [correct_planet] + decoy_planets
        # scramble each
        self.anagrams = {p: scramble(p) for p in self.all_planets}

    def play(self):
        print("\nAgent: Great, so we have these planets left. But what are these names!?")
        print("Agent: Ah, we have to find the name of the correct planet!")
        print("Agent: But, be careful, we have only one chance... The invaders are close...")
        for i, p in enumerate(self.all_planets, 1):
            print(f"{i}. {self.anagrams[p]}")  # show scrambled

        guess = input("\nName of the alien planet: ").strip().upper()
        if guess == self.correct_planet:
            print(f"\nAgent: Amazing! The aliens live on {self.correct_planet}. Earth is safe!")
            return self.correct_planet
        else:
            print("\nAlien 1: kdsaf! sdjfpwe jsospe sd oew jfsw. sjfoie sodfw js!")
            print("Translation: Wrong! Humans failed to find the planet. Earth is lost!")
            print("Alien 2: Wej jfsoeo!")
            print("Translation: Let's attack!")
            print("\nGAME OVER")
            return None  # End the game immediately


puzzle = SpectralTypePuzzle()
filtered_stars = puzzle.play(stars)

target_index = 3  # corresponding to the star with sum of digits 81
equation_text = r"\left( 3 \times 7 + \sqrt{196} \right) \cdot 2 + 1331^{1/3}"

math_puzzle = MathPuzzle(filtered_stars, target_index, equation_text)
correct_star = math_puzzle.play()

correct_planet = "The Right One"
decoy_planets = ["Not This One", "Absolute No", "Inconclusive", "Silly Humans"]
planet_puzzle = PlanetAnagramPuzzle(correct_planet, decoy_planets)
alien_planet = planet_puzzle.play()


# In[ ]:





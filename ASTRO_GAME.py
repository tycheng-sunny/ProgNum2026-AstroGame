#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random
import time
import math
from IPython.display import clear_output

# 1.The card class is defined
class Card:
    """Represents a single playing card with a suit, rank, and numeric value."""
    def __init__(self, suit, rank):
        #WE save the suit (ex: 'Stars') an the rank (ex: 'A') inside each card
        self.suit, self.rank = suit, rank
        # Dictionary to convert the text of the rank into a real number to alculate points
        val_map = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':11,'Q':12,'K':13,'A':14}
        self.value = val_map[rank]      
        # We define the  icons of the cards
        icons = {'Planets': '🪐', 'Stars': '⭐', 'Galaxies': '🌀', 'Black Holes': '🕳️'}
        self.icon = icons.get(suit, '?')
    def get_ascii(self):
        # Here, it is defined how the cards will look like during the game
        r = self.rank.ljust(2)
        return ["┌─────┐", f"│{r}   │", f"│  {self.icon} │", f"│   {r}│", "└─────┘"]
# The class item is defined(Upgrades and Jokers)
class Item:
    """Represents an upgrade (Joker or Nebula) that modifies the score multiplier."""
    # The item recieves a name, (joker ,nebula...), power, price and description
    def __init__(self, name, it_type, value, price, desc=""):
        self.full_name, self.type, self.value, self.price, self.desc = name, it_type, value, price, desc
        # Visual sign is defined:
        self.symbol = "🃏" if it_type == 'joker' else "✨"
    # MHOw to draw the object in the screen (ASCII art)
    def get_ascii(self):
        # We prepare the text value: if it is a  Joker, 'x' (multiplies), 
        # if it is not,  '+' (sum to the total multiplier)
        v_disp = f"x{self.value}" if self.type == 'joker' else f"+{self.value}"
        n_disp = self.full_name[:7].center(7)
        return ["┌───────┐", f"│{self.symbol}     │", f"│{n_disp}│", f"│{v_disp.center(7)}│", "└───────┘"]

# 2. A.L.I. = Automated Logic Interface
# We define the engine of the game, BalatroOdyssey contains all the rules
class BalatroOdyssey:
    """Main game engine handling the logic, scoring, and UI of the mission."""
    # These are the points of each hand 
    # The dictionary defines and relates the name of the hands with the values
    BASE_SCORES = {"COSMIC STR. FLUSH": 1000, "GALACTIC POKER": 800, "FULL HOUSE": 600, 
                   "NEBULA FLUSH": 500, "ORBITAL STRAIGHT": 400, "ASTEROID TRIO": 300,
                   "TWO PAIR": 200, "PLANETARY PAIR": 100, "High Card": 20}
# Here A.L.I. prepare the system once you start running the game
    def __init__(self):
        # At the beginning we start with 6 galactic $ and no objects.
        self.money, self.inventory = 6, []
        self.suits, self.ranks = ['Planets', 'Stars', 'Galaxies', 'Black Holes'], ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        # Every line is a dictionary with a context (ctx), formula (f), data (d), question (t) and answer (a).
        self.science_pool = [
            {"ctx": "Jupiter vs Earth mass ratio.", "f": "Mj / Me", "d": "Mj = 1.89819e27 kg, Me = 5.97219e24 kg", "t": "Earths in Jupiter?", "a": 1.89819e27 / 5.97219e24},
            {"ctx": "Wien's Law: Stellar peak.", "f": "T = 0.00289777 / lambda", "d": "lambda = 5.02e-7 m", "t": "T in Kelvin?", "a": 0.00289777 / 5.02e-7},
            {"ctx": "Hubble's Expansion.", "f": "d = v / H0", "d": "v = 15400 km/s, H0 = 67.4 km/s/Mpc", "t": "d in Mpc?", "a": 15400 / 67.4},
            {"ctx": "Kepler's 3rd Law (Jupiter Orbit).", "f": "P = sqrt(a^3)", "d": "a = 5.20336 AU", "t": "P in Earth years?", "a": math.sqrt(5.20336**3)},
            {"ctx": "Stefan-Boltzmann Luminosity.", "f": "L = 4*pi*R^2 * sigma * T^4", "d": "R=6.957e8m, sigma=5.67037e-8, T=5772K", "t": "L in Watts?", "a": 4 * math.pi * (6.957e8)**2 * 5.67037e-8 * (5772**4)},
            {"ctx": "Distance Modulus (Vega).", "f": "M = m - 5*log10(d/10)", "d": "m = 0.03, d = 7.68 pc", "t": "Absolute Mag (M)?", "a": 0.03 - 5 * math.log10(7.68 / 10)},
            {"ctx": "Radio delay (Mars-Earth).", "f": "t = d / c", "d": "d = 7.834e10 m, c = 299792458 m/s", "t": "t in seconds?", "a": 7.834e10 / 299792458},
            {"ctx": "Parallax to distance.", "f": "d = 1 / p", "d": "p = 0.76813 arcsec", "t": "d in parsecs?", "a": 1 / 0.76813},
            {"ctx": "Neutron Star Density.", "f": "rho = M / (4/3 * pi * R^3)", "d": "M = 2.78e30 kg, R = 12000 m", "t": "rho in kg/m^3?", "a": 2.78e30 / (4/3 * math.pi * 12000**3)},
            {"ctx": "Photon Energy.", "f": "E = (h * c) / lambda", "d": "h=6.626e-34, c=299792458, lambda=5.5e-7", "t": "E in Joules?", "a": (6.626e-34 * 299792458) / 5.5e-7}
        ]
        random.shuffle(self.science_pool)
        # The "joker_pool" are the supermassive BH that act as Jokers.
        # Each one has a real BH name, tipe, multiplier ans price.
        self.joker_pool = [Item("SagitA", "joker", 1.5, 4), Item("M87", "joker", 2, 7),
                           Item("NGC1277", "joker", 2.5, 10), Item("Gargan", "joker", 3, 13),
                           Item("TON618", "joker", 4, 18), Item("PhoenixA", "joker", 5, 25)]
        # The same for the boost
        self.boost_pool = [Item("CrabNeb", "nebula", 2, 6, "+2 Mult global"),
                           Item("Pillars", "nebula", 3, 9, "+3 Mult global"),
                           Item("C.Sagan", "special", 2, 8, "x2 if Pair"),
                           Item("S.Hawk", "special", 5, 10, "+5 Mult if Joker"),
                           Item("Hubble", "special", 3, 12, "x3 if Flush")]

    #This is the Ali communication system
    def ship_log(self, text, speed=0.03):
        print("🤖 [A.L.I]: ", end="")
        for char in text:
            # Print the current character. 'flush=True' forces it to appear on screen immediately]
            print(char, end="", flush=True); time.sleep(speed)
        print("\n")
        
    # Intro manage the beggining of the hustory and the rules
    def intro(self):
        clear_output()
        self.ship_log("Welcome, Commander. Awakening from cryo-sleep...")
        self.ship_log("THE STORY: The universe has reached heat death. We are the last ship, carrying the 'Genesis Core'.")
        self.ship_log("Our goal is the Final Singularity. We must feed it enough energy to trigger a new Big Bang.")
        print("\n" + "═"*50)
        print("THE MISSION PROTOCOLS:")
        print("1. ENERGY: Generated by playing 5-card Poker hands.")
        print("2. FUEL (HANDS): You have 4 per sector.")
        print("3. DISCARDS: You have 3 per sector.")
        print("═"*50 + "\n")
        input("[ Press Enter to Initiate Engine Ignition ]")
        
    def draw_ui(self, r_num, goal, score, hands, discs, hand):
# This method renders the entire visual interface displayed on the game screen  
        clear_output(wait=True)
        locs = ["Oort Cloud Border", "Nebula Pillars", "Andromeda Edge", "Great Attractor", "EVENT HORIZON"]
        #(r_num-1 because lists start at 0)
        print(f"🛰️  STARSHIP STATUS | SECTOR: {locs[r_num-1]}")
        print(f"⚡ CORE ENERGY: {score}/{goal} | ✋ HANDS: {hands} | ♻️ DISCS: {discs} | $: {self.money}")
        if self.inventory:
            # Gets the ASCII drawing (the 5-line list) of each object you own
            inv_ascii = [i.get_ascii() for i in self.inventory]
            # Loop to print the 5 lines of height for the objects, one next to the other
            for line in range(5): print("  ".join(it[line] for it in inv_ascii))
        print("\n" + "═"*75)
        # Creates a text list with the names of the poker hands and their base points
        base_info = [f"{k}: {v}" for k, v in self.BASE_SCORES.items()]
        # Adjustment to avoid errors if the hand is small
        rows = [hand[0:4], hand[4:8]]
        idx_s = 0
        # Loop to process each of the two rows of cards
        for i_row, row in enumerate(rows):
            if not row: continue
            ascii_cards = [c.get_ascii() for c in row]
            # Cards are 5 lines high; this loop iterates through them one by one
            for i_line in range(5):
                # Joins the card segments of that line with spaces ("   ")
                cards_part = "   ".join(c[i_line] for c in ascii_cards)
                info_part = f"    ║ {base_info[i_line + (i_row*5)]}" if (i_line + (i_row*5)) < len(base_info) else ""
                print(f"{cards_part}{info_part}")
            print("  ".join(f"  ({idx_s + j})   " for j in range(len(row))) + "\n")
            idx_s += 4
        print("═"*75)

    def calculate_score(self, cards):
        """Analyses the hand, identifies the poker rank, and applies multipliers."""
        if not cards: return 0, "None"
        # Extracts the card numbers and sorts them; extracts the suits into another list
        v = sorted([c.value for c in cards]); s = [c.suit for c in cards]
        # Counts how many times each number repeats and stores the count (e.g., a trio stores a 3)
        counts = {val: v.count(val) for val in set(v)}; sorted_c = sorted(counts.values(), reverse=True)
        # Check for FLUSH (all suits identical) and STRAIGHT (5 consecutive numbers)
        is_f = len(set(s)) == 1 and len(cards) == 5; is_s = len(set(v)) == 5 and (max(v) - min(v) == 4)
        base, name = 20, "High Card"
        if is_s and is_f: base, name = 1000, "COSMIC STR. FLUSH"
        elif sorted_c[0] == 4: base, name = 800, "GALACTIC POKER"
        elif sorted_c[0] == 3 and (len(sorted_c)>1 and sorted_c[1]==2): base, name = 600, "FULL HOUSE"
        elif is_f: base, name = 500, "NEBULA FLUSH"
        elif is_s: base, name = 400, "ORBITAL STRAIGHT"
        elif sorted_c[0] == 3: base, name = 300, "ASTEROID TRIO"
        elif sorted_c[0] == 2 and (len(sorted_c)>1 and sorted_c[1]==2): base, name = 200, "TWO PAIR"
        elif sorted_c[0] == 2: base, name = 100, "PLANETARY PAIR"
        
        mult = 1
        for it in self.inventory:
            if it.type == "nebula": mult += it.value
            if any(i.type == "joker" for i in self.inventory) and it.full_name == "S.Hawk": mult += 5
            if it.type == "joker": mult *= it.value
            if it.full_name == "C.Sagan" and "PAIR" in name: mult *= 2
            if it.full_name == "Hubble" and "FLUSH" in name: mult *= 3
        return int(base * mult), name
# This method runs a single sector (round) of the game
    def play_round(self, r_num, goal):
        """Handles the logic of a single sector, including turns, plays, and discards."""
        score, hands, discs = 0, 4, 3
        # Generate a full deck of 52 cards (combining every suit with every rank)
        deck = [Card(s, r) for s in self.suits for r in self.ranks]
        random.shuffle(deck)
        # Initialize the player's hand and the discard pile
        hand, discard_pile =[], []
# Draw cards until the hand has 8 cards or the deck is empty
        while len(hand) < 8 and deck:
            hand.append(deck.pop())
# Main gameplay loop: continues until the goal is met or you run out of hands
        while score < goal and hands > 0:
            self.draw_ui(r_num, goal, score, hands, discs, hand)
            
            action = input("🤖 (p)lay / (d)iscard: ").lower().strip()
 # Clean the input: keep only digits, ensure they are within hand range, and sort them backwards
     # (We sort reverse=True so popping index 5 doesn't change the position of index 2)
            if action not in ['p', 'd']: continue
            if action == 'd' and discs <= 0:
                print("🚫 NO DISCARDS!"); time.sleep(1); continue

            try:
                raw_input = input("🤖 INDICES (0-7): ").replace(',', ' ').split()
                sel_idxs = sorted([int(i) for i in raw_input if i.isdigit() and int(i) < len(hand)], reverse=True)
                if not sel_idxs: continue
                if len(sel_idxs) > 5:
                    print("⚠️ MAX 5 CARDS!"); time.sleep(1); continue
                # Remove the selected cards from the hand and store them in 'selected_cards'
                selected_cards = [hand.pop(i) for i in sel_idxs]
                
                if action == 'p':
                    pts, name = self.calculate_score(selected_cards)
                    score += pts
                    hands -= 1
                    print(f"✨ {name}! +{pts} energy")
                    discard_pile.extend(selected_cards)
                    time.sleep(1.5)
                else:
                    discs -= 1
                    discard_pile.extend(selected_cards)
                    print(f"♻️ Discarding {len(selected_cards)} cards...")
                    time.sleep(0.8)

                while len(hand) < 8:
                    if not deck:
                        if not discard_pile: break
                        deck = discard_pile[:]
                        discard_pile.clear()
                        random.shuffle(deck)
                    if deck:
                        hand.append(deck.pop())
            except: continue

        if score >= goal:
            # A.L.I. logs the success of the current mission sector
            self.ship_log(f"Sector {r_num} Clear.")
            self.money += 5
            time.sleep(1)
            # If this wasn't the final sector (Sector 5), prepare for the next jump
            if r_num < 5:
                # Check if the Science Lab exists, then trigger the math/physics challenge
                if hasattr(self, 'run_science_lab'): self.run_science_lab()
                self.run_shop()
            return True
        return False

    def run_science_lab(self):
        """Presents a physics challenge to earn credits based on numerical accuracy."""
        if not self.science_pool: return
        # Take the last challenge from the randomized pool (pop removes it so it's not repeated)
        prob = self.science_pool.pop()
        clear_output(wait=True); self.ship_log("Diverting power to the Science Lab.")
        print(f"\nSITUATION: {prob['ctx']}\nFORMULA: {prob['f']}\nDATA: {prob['d']}")
        try:
            ans = float(input(f"\nRESULT ({prob['t']}): "))
            # ACCURACY CHECK: If the answer is within a 10% margin of error (0.9 to 1.1)
            # This allows for small rounding differences in the Commander's calculations
            if prob['a'] * 0.9 <= ans <= prob['a'] * 1.1:
                self.money += 12; self.ship_log("Calculation verified. +$12 Credits.")
                # Failure: Display the correct value in scientific notation
            else: self.ship_log(f"Calculation error. Correct value: {prob['a']:.4e}")
        except: self.ship_log("Nav-computer error.")
        time.sleep(1.5)
       # This method manages the shopping phase between mission sectors
    def run_shop(self):
        """Displays available upgrades for purchase and handles transaction logic."""
        stock = random.sample(self.joker_pool, 3) + random.sample(self.boost_pool, 2)
        # Shop loop: stays open until the Commander decides to leave or an error occurs
        while True:
            clear_output(wait=True)
            print(f"🛒 SHOP | $: {self.money}")
            # List all items in the current stock with their price and description
            for i, it in enumerate(stock):
                # .ljust(10) ensures the names are aligned in a neat column
                print(f"{i+1}. {it.full_name.ljust(10)} | ${it.price} | {it.desc or 'x'+str(it.value)}")
            sel = input("\nBuy (1-5) or 0 to Exit: ")
            # Exit condition: if the user types '0', we break the loop and leave the shop
            if sel == '0': break
            try:
                # CHECKING CONDITIONS: 
                # 1. Index is valid. 2. Enough money. 3. Inventory has space (max 5 items).
                idx = int(sel)-1
                if 0 <= idx < len(stock) and self.money >= stock[idx].price and len(self.inventory) < 5:
                    self.money -= stock[idx].price
                    self.inventory.append(stock.pop(idx))
            except: break

    def start(self):
        """Launches the game and iterates through the 5 sectors of the mission."""
        self.intro()
        goals = [500, 2000, 6000, 15000, 40000]
        for i, g in enumerate(goals):
            if not self.play_round(i+1, g):
                clear_output(); self.ship_log("ENERGY CRITICAL... MISSION FAILED.")
                return
        clear_output()
        self.ship_log("GENESIS CORE IGNITED! NEW UNIVERSE BORN!")
        print("\n" + "💥"*15 + "\n    🌟 LET THERE BE LIGHT 🌟\n" + "💥"*15)

BalatroOdyssey().start()


# # 

# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import sys

# --- DATABASES ---
UPGRADE_DATABASE = {
    "Advanced Sensors": {"cost": 25, "effect": "Reduces Survey costs by 50%", "id": "U1"},
    "High-Efficiency Drills": {"cost": 40, "effect": "+20% Success Probability", "id": "U2"},
    "Nuclear Thrusters": {"cost": 30, "effect": "Reduces Operation travel time by 1 turn", "id": "U3"},
    "PR Department": {"cost": 20, "effect": "Reduces audit penalty by 3", "id": "U4"},
    "Bribe the Auditor": {"cost": 50, "effect": "Delays the 'Suits' audit by 3 turns", "id": "U5"},
    "Automated Refineries": {"cost": 60, "effect": "Gain +1 Fund every turn passively", "id": "U6"},
    "Deep Space Relay": {"cost": 35, "effect": "Surveys complete instantly", "id": "U7"}
}

SYSTEM_DATABASE = {
    "Proxima Centauri": {"distance": 4.2, "planets": {"Proxima b": {"cost": 5, "reward": 15, "base_chance": 0.8}, "Proxima c": {"cost": 8, "reward": 25, "base_chance": 0.6}}},
    "Barnard's Star": {"distance": 6.0, "planets": {"Barnard b": {"cost": 6, "reward": 20, "base_chance": 0.75}}},
    "Wolf 359": {"distance": 7.8, "planets": {"Wolf b": {"cost": 10, "reward": 30, "base_chance": 0.55}}},
    "Lalande 21185": {"distance": 8.3, "planets": {"Lalande b": {"cost": 12, "reward": 35, "base_chance": 0.5}}},
    "Sirius": {"distance": 8.6, "planets": {"Sirius b": {"cost": 15, "reward": 45, "base_chance": 0.4}}},
    "Luyten 726-8": {"distance": 8.7, "planets": {"Luyten a": {"cost": 7, "reward": 22, "base_chance": 0.7}}},
    "Ross 154": {"distance": 9.7, "planets": {"Ross b": {"cost": 9, "reward": 28, "base_chance": 0.65}}},
    "Epsilon Eridani": {"distance": 10.5, "planets": {"AEgir": {"cost": 14, "reward": 40, "base_chance": 0.5}}},
    "Tau Ceti": {"distance": 11.9, "planets": {"Tau e": {"cost": 18, "reward": 50, "base_chance": 0.5}, "Tau f": {"cost": 18, "reward": 55, "base_chance": 0.45}}},
    "Vega": {"distance": 25.0, "planets": {"Vega Prime": {"cost": 30, "reward": 100, "base_chance": 0.3}}},
    "Arcturus": {"distance": 36.7, "planets": {"Bootes Gamma": {"cost": 50, "reward": 200, "base_chance": 0.25}}},
    "Altair": {"distance": 16.7, "planets": {"Altair IV": {"cost": 22, "reward": 70, "base_chance": 0.4}}},
    "Fomalhaut": {"distance": 25.1, "planets": {"Sauron's Eye": {"cost": 35, "reward": 120, "base_chance": 0.35}}},
    "Deneb": {"distance": 100.0, "planets": {"Cygnus X-1": {"cost": 150, "reward": 600, "base_chance": 0.15}}}
}

EVENT_DATABASE = [
    {"name": "Market Boom", "desc": "Precious metal prices spike! +10 Funds.", "effect": "funds", "value": 10},
    {"name": "Crew Morale Boost", "desc": "Extra rations and a movie night. +10 Morale.", "effect": "morale", "value": 10},
    {"name": "Optimized Routes", "desc": "Navigational breakthrough! Active ops speed up.", "effect": "eta", "value": -1},
    {"name": "Found Space Debris", "desc": "Salvaged an old satellite. +5 Funds.", "effect": "funds", "value": 5}
]

CRISIS_DATABASE = [
    {"name": "Solar Flare", "desc": "Equipment damage! -8 Funds for repairs.", "effect": "funds", "value": -8},
    {"name": "Space Sickness", "desc": "The crew is feeling the isolation. -12 Morale.", "effect": "morale", "value": -12},
    {"name": "Engine Glitch", "desc": "Active missions are delayed.", "effect": "eta", "value": 1},
    {"name": "Bureaucratic Red Tape", "desc": "Legal fees and audits. -5 Funds.", "effect": "funds", "value": -5}
]

class SpaceProspectorGame:
    def __init__(self, name):
        self.game_name = name
        self.is_running = False
        self.turn_count = 0
        self.funds = 0
        self.morale = 0
        self.deadline = 0
        self.last_success_turn = -10
        self.audit_delay = 0 
        self.debt_turns = 0
        self.misery_turns = 0
        self.investigated_systems = []
        self.accessible_systems = list(SYSTEM_DATABASE.keys())
        self.pending_investigations = []
        self.active_operations = []
        self.upgrades_owned = []

    def start_menu(self): #Code for the start menu, nothing special
        print(f"\n{'='*40}\nWelcome to {self.game_name}!\n{'='*40}")
        while not self.is_running:
            choice = input("\n[S] Start Game | [H] Help > ").upper()
            if choice == "S":
                self.is_running = True
                self.setup_game() 
                self.play_turn()   
            elif choice == "H":
                print(f"\n--- OFFICIAL PROSPECTOR MANUAL ---")
                print(f"GOAL: Maintain positive Funds and Morale while surveying stars.")
                print(f"\nCOMMANDS:")
                print(f"[1] SURVEY: Map stars to later be able to mine them")
                print(f"[2] MINE: Launch operations. High difficulty/distance gives more morale on success.")
                print(f"[3] UPGRADES: Tech improvements. No currency symbols used in costs.")
                print(f"[4] EMERGENCY SCAN: Quick funds (+5) at a morale cost (-10).")
                print(f"\nWARNINGS:")
                print(f"- Audits and Crises begin on Turn 5.")
                print(f"- 3 consecutive turns of negative Funds or Morale results in mission failure.")

    def setup_game(self): #Starting the game
        self.funds = int(np.random.randint(60, 90)) 
        self.morale = 80 
        self.deadline = int(np.random.randint(6, 12))
        self.investigated_systems = list(np.random.choice(self.accessible_systems, size=4, replace=False))

    def display_stats(self, context="LIVE"): #So that the stats are displayed each time they're changed
        print(f"\n>>> [{context}] Funds: {self.funds} | Morale: {self.morale} | Deadline: {self.deadline}")
        if self.funds < 0: print(f"    [!] BANKRUPTCY WARNING: {3 - self.debt_turns} turns left")
        if self.morale < 0: print(f"    [!] MUTINY WARNING: {3 - self.misery_turns} turns left")

    def check_lose_conditions(self): #See if the game has ended 
        if self.funds < 0: self.debt_turns += 1
        else: self.debt_turns = 0
        if self.morale < 0: self.misery_turns += 1
        else: self.misery_turns = 0

        if self.debt_turns >= 3:
            print("\n" + "!"*60 + "\nGAME OVER: FINANCIAL INSOLVENCY\nThe institute has been shut down due to poor performance.\n" + "!"*60)
            sys.exit()#Straight up kills the program
        if self.misery_turns >= 3:
            print("\n" + "!"*60 + "\nGAME OVER: TOTAL MUTINY\nYou lost yourself to greed, you team left. No one wants to work with you.\n" + "!"*60)
            sys.exit()#Straight up kills the program

    def handle_encounters(self):#Generates random events and crises
        if np.random.random() < 0.8:
            crisis = np.random.choice(CRISIS_DATABASE)
            print(f"\n[CRISIS] {crisis['name']}: {crisis['desc']}")
            if crisis['effect'] == "funds": self.funds += crisis['value']
            elif crisis['effect'] == "morale": self.morale += crisis['value']
            elif crisis['effect'] == "eta":
                for op in self.active_operations: op['turns_left'] += crisis['value']
            self.display_stats("CRISIS")

        if np.random.random() < 0.6:
            event = np.random.choice(EVENT_DATABASE)
            print(f"\n[EVENT] {event['name']}: {event['desc']}")
            if event['effect'] == "funds": self.funds += event['value']
            elif event['effect'] == "morale": self.morale = min(100, self.morale + event['value'])
            elif event['effect'] == "eta":
                for op in self.active_operations: op['turns_left'] = max(1, op['turns_left'] + event['value'])
            self.display_stats("EVENT")

    def play_turn(self): #Turn logic (ts is very long)
        self.turn_count += 1
        self.check_lose_conditions()#See if you lose
        depletion = 2 
        if "Automated Refineries" in self.upgrades_owned: depletion -= 1
        if self.turn_count >= 5:#For audits so that you can't just pass
            if not (self.turn_count - self.last_success_turn <= 2 and self.deadline <= 0): 
                if self.audit_delay > 0:
                    self.audit_delay -= 1
                else:
                    audit_penalty = 5
                    if "PR Department" in self.upgrades_owned: audit_penalty -= 3
                    depletion += audit_penalty
                    print(f"!!! AUDIT ACTIVE: -{audit_penalty} Funds.")
            self.handle_encounters()

        self.funds -= depletion#Cost of new turn(May change)
        
        for sys_name in self.pending_investigations: self.investigated_systems.append(sys_name) #list with investigated systems
        self.pending_investigations = [] 
        
        completed_ops = [] 
        for op in self.active_operations: #Logic for operations 
            op["turns_left"] -= 1
            if op["turns_left"] <= 0:
                roll = np.random.random()
                if roll <= op["success_chance"]:
                    print(f"\n[SUCCESS] {op['planet']} complete! Collected {op['reward']} funds.")
                    self.funds += op["reward"]
                    self.last_success_turn = self.turn_count
                    m_gain = int((1 - op["success_chance"]) * 30 + (op["distance"] / 4))
                    self.morale = min(100, self.morale + m_gain)
                    print(f"Success! Morale +{m_gain}")
                else:
                    print(f"\n[FAILURE] Expedition to {op['planet']} failed.")
                    if op["success_chance"] > 0.80:
                        self.morale -= 15
                        print("Crew frustration (Failure on >80%): Morale -15") #If we fail an easy operation we lose morale
                self.display_stats("MISSION RESULT")
                completed_ops.append(op)
        for op in completed_ops: self.active_operations.remove(op)#So that you cannot do the same one time and time again
            
        if self.deadline > 0: self.deadline -= 1
        
        print("\n" + "="*60)
        print(f"TURN {self.turn_count} SUMMARY")
        self.display_stats("TURN END")
        print("-" * 20 + "\nACTIVE MISSIONS:")
        if not self.active_operations: print("- No active missions.")
        else:
            for op in self.active_operations:
                print(f"- {op['planet']} ({op['system']}): {op['turns_left']} turn(s) left")
        print("-" * 20)
        self.operations()

    def operations(self): #The logic for what you can do in a turn
        print("\n[1] Survey | [2] Mine | [3] Upgrades | [4] Scan | [5] Pass")
        self.Action = input("> ")
        while True:
            if self.Action == "5": self.play_turn(); break
            elif self.Action == "1":#Logic to research systems
                print("\n--- RESEARCH CENTER ---")
                for sys_name in self.accessible_systems:
                    cost = int(SYSTEM_DATABASE[sys_name]["distance"] * 5)
                    if "Advanced Sensors" in self.upgrades_owned: cost //= 2
                    status = "[MAPPED]" if sys_name in self.investigated_systems else f"[Cost: {cost}]"
                    print(f"- {sys_name}: {status}")
                target = input("System to Research (or 'Back'): ")
                if target in self.accessible_systems and target not in self.investigated_systems:
                    cost = int(SYSTEM_DATABASE[target]["distance"] * 5)
                    if "Advanced Sensors" in self.upgrades_owned: cost //= 2
                    if self.funds >= cost:
                        self.funds -= cost
                        if "Deep Space Relay" in self.upgrades_owned: self.investigated_systems.append(target)
                        else: self.pending_investigations.append(target)
                        print(f"Survey of {target} initialized.")
                        self.display_stats("POST-SURVEY")
                    else: print("Insufficient funds.")
                elif target == "Back": self.operations(); break
                self.Action = input("> ")

            elif self.Action == "2": #Logic to mine planets
                print("\n--- PROSPECTING ---")
                for sys_name in self.investigated_systems:
                    print(f"[{sys_name}]")
                    for p, d in SYSTEM_DATABASE[sys_name]['planets'].items():
                        eta = max(1, int(SYSTEM_DATABASE[sys_name]['distance'] / 3))
                        if "Nuclear Thrusters" in self.upgrades_owned: eta = max(1, eta - 1)
                        chance = d['base_chance'] + np.random.uniform(-0.03, 0.03)
                        if "High-Efficiency Drills" in self.upgrades_owned: chance += 0.20
                        print(f"  > {p}: Cost: {d['cost']} | Reward: {d['reward']} | Chance: {int(chance*100)}% | ETA: {eta}")
                
                target_sys = input("\nSystem (or 'Back'): ")
                if target_sys in self.investigated_systems:
                    target_p = input(f"Planet: ")
                    if target_p in SYSTEM_DATABASE[target_sys]['planets']:
                        p_data = SYSTEM_DATABASE[target_sys]['planets'][target_p]
                        if self.funds >= p_data['cost']:
                            self.funds -= p_data['cost']
                            eta = max(1, int(SYSTEM_DATABASE[target_sys]['distance'] / 3))
                            if "Nuclear Thrusters" in self.upgrades_owned: eta = max(1, eta - 1)
                            final_chance = p_data['base_chance'] + (0.2 if "High-Efficiency Drills" in self.upgrades_owned else 0)
                            self.active_operations.append({
                                "system": target_sys, "planet": target_p, "turns_left": eta, 
                                "reward": p_data['reward'], "success_chance": final_chance, 
                                "distance": SYSTEM_DATABASE[target_sys]['distance']
                            })
                            print(f"Launch confirmed for {target_p}.")
                            self.display_stats("POST-LAUNCH")
                        else: print("Insufficient funds.")
                elif target_sys == "Back": self.operations(); break
                self.Action = input("> ")

            elif self.Action == "3":#Logic for Upgrades
                print("\n--- TECH TREE ---")
                for n, d in UPGRADE_DATABASE.items():
                    cost_display = f"[Cost: {d['cost']}]" if n not in self.upgrades_owned else "[OWNED]"
                    print(f"- {n}: {d['effect']} {cost_display}")
                choice = input("Select Upgrade (or 'Back'): ")
                if choice in UPGRADE_DATABASE and choice not in self.upgrades_owned:
                    if self.funds >= UPGRADE_DATABASE[choice]['cost']:
                        self.funds -= UPGRADE_DATABASE[choice]['cost']
                        self.upgrades_owned.append(choice)
                        if choice == "Bribe the Auditor": self.audit_delay += 3
                        print(f"{choice} installed.")
                        self.display_stats("POST-UPGRADE")
                    else: print("Not enough funds.")
                elif choice == "Back": self.operations(); break
                self.Action = input("> ")

            elif self.Action == "4":
                if self.morale >= 10: 
                    self.morale -= 10
                    self.funds += 5
                    print("Emergency scan sold: +5 Funds, -10 Morale.")
                    self.display_stats("POST-SCAN")
                else: print("Crew too demoralized.")
                self.Action = input("> ")
            else: self.Action = input("> ")

if __name__ == "__main__":
    game = SpaceProspectorGame("Starbound Prospector")
    game.start_menu()


# In[ ]:





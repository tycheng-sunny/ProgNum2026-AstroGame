# %%

import numpy as np 
from astropy.io import fits 
from matplotlib.pyplot import show, figure, subplots
import time
import sys

def t_print(text, speed=0.03):
    """Function to print text with a typewriter effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()  

class Cafeteria:
    """Defines what you see in the cafeteria"""

    def __init__(self):
        t_print("\nAs you walk into the cafetaria, it's pure chaos")
        t_print("Every branch of the ship which doesn't hold personel for the control room connects here")
        t_print("People are running around and screaming trying to find their way towards the escape pods")
        t_print("As you get pushed aside you decide it's time to get out of here")


class Puzzle1:
    """Puzzle for getting into the control room"""

    def __init__(self):
        t_print("\nYou take a closer look at the keypad and notice that there is a note taped to the side of it")
        t_print("On the note it says: ")
        t_print("The code to open the control room corresponds to")
        t_print("the RA and DEC of the given HI-map where we find the highest intensity")
        t_print("Tip: Round to tens")
        t_print("Attached to the note is a picture: ")
        self.HI_map()

    def HI_map(self):
        # Calculating and plotting the HI-map using a dataset from the course

        # Reading fits file and converting to data array
        ngc_list = fits.open('ngc6946.fits')
        dat = ngc_list[0].data
        data = np.asarray(dat)

        # Calculating HI map
        total_HI = np.sum(data[2:67], axis=0)
        x = np.arange(0, 100, 10)

        fig, ax = subplots()
        Image = ax.imshow(total_HI)

        # Labelling axes with CTYPE1 and CTYPE2
        hdr = ngc_list[0].header
        ax.set_xlabel(rf'{hdr["CTYPE1"]}')
        ax.set_ylabel(rf'{hdr["CTYPE2"]}')
        ax.set_xticks(x)
        ax.grid(True, linestyle='--', color='k')

        # Creating colorbar and label with BUNIT
        
        cbar = fig.colorbar(Image)
        cbar.set_label(rf"{hdr['BUNIT']}")

        show()

class Stations:
    """Descriptions of the stations in the control room"""

    def __init__(self):
        t_print("Each station is located in a different part of the control room")
        self.Station1()
        self.Station2()
        self.Station3()
        self.Station4()
        
    def Station1(self):
        t_print("\nStation 1 is located right next to you")
        t_print("Above the station hangs a planet, and a sign that says: ")
        t_print("               PLANETARY NAVIGATION")
    
    def Station2(self):
        t_print("\nStation 2 is located in the back corner of the control room")
        t_print("On the station are a bunch of graphs and a sign that says: ")
        t_print("                     SIGNAL ANALYSIS")
    
    def Station3(self):
        t_print("\nStation 3 is located exactly mirrored to Station 1")
        t_print("Above the station hangs a star, and a sign that says: ")
        t_print("               STELLAR NAVIGATION")
    
    def Station4(self):
        t_print("\nStation 4 is located in the middle of the control room")
        t_print("On this station there is a holographic projection of constellations and a sign that says: ")
        t_print("                           STELLAR MAPPING")


class Puzzle2:
    """Puzzle for station 1, planetary navigation"""

    def __init__(self):
        t_print("\nYou walk up to station 1 and examine the screen")
        t_print("'PLANET NAVIGATION DISRUPTED'")
        t_print("The screen shows the order in which the planets orbit around our Sun")
        t_print("Venus, Jupiter, Mars, Saturn, Mercury, Neptune, Earth, Uranus")
        self.objective()

    def objective(self):
        t_print("To reset the station you need to realign the planets in the correct order")
        t_print("Input the first letter of each planet in the correct order on the screen")

class Puzzle3:
    """Puzzle for station 2, signal analysis"""

    def __init__(self):
        t_print("\nYou walk up to station 2 and examine the screen")
        t_print("SIGNAL ANALYSIS DISRUPTED")
        t_print("UNKOWN SIGNAL DETECTED")
        self.objective()
        self.signal()

    def objective(self):
        t_print("\nTo reset the station you need to identify the signal by identifying signal anomalies")
        t_print("Input the spots on the graph where the signal peaks")
        t_print("Hint: The peaks create a sequence of 8 numbers")
    
    def signal(self):
        # Plotting a signal with peaks

        data = np.random.uniform(0, 3, 100)
        x = np.arange(0, len(data), 1)

        fig, ax = subplots()
        ax.stem(x, data, markerfmt='')
        ax.axvline(x=20, ymin=0, ymax=0.5)
        ax.axvline(x=45, ymin=0, ymax=0.62)
        ax.axvline(x=70, ymin=0, ymax=0.49)
        ax.axvline(x=95, ymin=0, ymax=0.55)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 7)
        ax.set_xticks(np.arange(0, 100, 10))
        show()

class Puzzle4:
    """Puzzle for station 3, stellar navigation"""

    def __init__(self):
        t_print("\nYou walk up to station 3 and examine the screen")
        t_print("STELLAR NAVIGATION DISRUPTED")
        t_print("REIDENTIFY SOLAR DESTINATION")
        self.objective()
        self.info()

        t_print("\nHint: The input should be: Spectral type-color-size spelled out. Example: B-blue-white-Supergiant")

    def objective(self):
        t_print("\nTo reset the station you need to identify which star is our Sun")
        t_print("Input the necessary information about the star to set the correct destination")
        t_print("We are given the following information: ")

    def info(self):
        print("\nSpectral type: \nO > 30000 K, B = 10000-30000 K, A = 7500-10000 K, F = 6000-7500 K, \nG = 5200-6000 K, K = 3700-5200 K, M = <3700 K")
        print("\nColor: \nO = blue, B = blue-white, A = white, F = yellow-white, G = yellow, K = orange, M = red")
        print("\nSize: \nO-M = Main sequence, G,K,M = Giant, D = White dwarf, O-M = Supergiant")
        
        
class Puzzle5:
    """Puzzle for station 4, stellar mapping"""    

    def __init__(self):
        t_print("\nYou walk up to station 4 and examine the error message")
        t_print("LOCATION LOST")
        t_print("REMAP STARS TO REGAIN LOCATION")
        self.objective()
        self.constellation1()

    def objective(self):
        t_print("\nTo reset the station you need to reidentify the constellations on the map")
        t_print("Input the correct constellation that is being projected on the screen")

    def failed_station(self):
        t_print("ERROR! ERROR! SYSTEM FAILURE")
        t_print("INITIATE SELF DESTRUCT")
        t_print("As you fail the code a second time the ship shudders")
        t_print("You lose your balance and fall to the ground")
        t_print("Then everything goes black as the ship explodes around you")

    """Working out constellation 1"""
    def constellation1(self):
        # Plotting constellation: Ursa Major
        x = [1, 3, 5, 7, 7.1, 12, 11.5]
        y = [2.5, 2.3, 2.1, 2, 1.6, 2, 1.5]

        fig, ax = subplots()
        ax.scatter(x, y, color='k', marker='*')
        ax.set_title("Constellation 1")
        ax.set_axis_off()
        show()

        Input = input("Input the name of the first constellation: ").lower().strip()
        self.constellation1_evaluation(Input)

    def constellation1_evaluation(self, Input):
        if Input == 'ursa minor' or Input == 'little dipper' or Input == 'little bear':
            t_print("CONSTELLATION 1 CORRECT")
            t_print("You have successfully identified constellation 1, you can now move on to the next constellation")
            self.constellation2()
        else:
            t_print("Wrong constellation; Try again")
            t_print("Hint: Most well known constellation in the northern hemisphere")
            Input_retry = input("Input the name of the first constellation: ").lower().strip()
            self.constellation1_retry(Input_retry)

    def constellation1_retry(self, Input):
        if Input == 'ursa minor' or Input == 'little dipper' or Input == 'little bear':
            t_print("CONSTELLATION 1 CORRECT")
            t_print("You have successfully identified constellation 1, you can now move on to the next constellation")
            self.constellation2()
        else:
            self.failed_station()


    """Working out constellation 2"""
    def constellation2(self):
        # Plotting constellation: Orion
        x = [1.5, 1.9, 1.6, 1.7, 1.8, 1.4, 1.3, 1.7, 1.85, 2.2, 2.19, 2.19, 2.15, 2.15, 2.12]
        y = [0, 0.2, 3.2, 3.4, 3.6, 6.5, 7.2, 7.3, 6, 6, 5.7, 6.4, 7, 5, 4.9]

        fig, ax = subplots()
        ax.scatter(x, y, color='k', marker='*')
        ax.set_title("Constellation 2")
        ax.set_axis_off()
        show()

        Input = input("Input the name of the second constellation: ").lower().strip()
        self.constellation2_evaluation(Input)

    def constellation2_evaluation(self, Input):
        if Input == 'orion':
            t_print("CONSTELLATION 2 CORRECT")
            t_print("You have successfully identified constellation 2, you can now move on to the next constellation")
            self.constellation3()
        else:
            t_print("Wrong constellation; Try again")
            t_print("Hint: Named after a Greek hunter")
            Input_retry = input("Input the name of the second constellation: ").lower().strip()
            self.constellation2_retry(Input_retry)

    def constellation2_retry(self, Input):
        if Input == 'orion':
            t_print("CONSTELLATION 2 CORRECT")
            t_print("You have successfully identified constellation 2, you can now move on to the next constellation")
            self.constellation3()
        else:
            self.failed_station()

    """Working out constellation 3"""
    def constellation3(self):
        # Plotting constellation: Pegasus
        x = [0.5, 0.7, 2, 2, 2.7, 2.5, 2.55, 2.7, 3.9, 3.7, 4.8, 4.8, 5.7, 4.8]
        y = [2, 4, 3.9, 2, 4.1, 3.3, 3.25, 0.8, 0.2, 3.7, 3.8, 2.5, 3, 0.8]

        fig, ax = subplots()
        ax.scatter(x, y, color='k', marker='*')
        ax.set_title("Constellation 3")
        ax.set_axis_off()
        show()




class Game:
    """Defining the text and possible choices"""

    def __init__(self):
        """Starts the game & defines where player has been and can't go back"""
        t_print("ERROR! ERROR! SHIP DESTABILIZED")
        t_print("ALL PERSONAL GO TO THE ESCAPE PODS")
        t_print("\nYou wake up and get out of bed")
        t_print("You know what to do, you have to be the one to stabilize the ship")

        # Track which stations have been reset
        self.stations_reset = {
            'Station 1': False,
            'Station 2': False,
            'Station 3': False,
            'Station 4': False
        }

    def start(self):
        """Gives the start of the game and the first choice"""
        t_print("\nYou find yourself in a room, it's your room")
        t_print("The room is small, it has a door right across from the bed")
        t_print("You go out into the hall, as people run past you to the left hall")
        t_print("You can either go left or right or you can stay in your room")
        choice1 = input("Where do you go(left, right or stay): ").lower().strip()
        self.first_choice(choice1)

    def first_choice(self, choice):
        """Evaluates the first choice"""
        if choice == 'left':
            self.left_hall()
        elif choice == 'right':
            self.right_hall()
        else:
            self.stay()

    def stay(self):
        """Gives final choice if you want to stay"""
        choice = input("\nAre you sure you don't want to do anything? ").lower().strip()
        self.stay_choice(choice)

    def stay_choice(self, choice):
        """Evaluates the choice to stay or not"""
        if choice == 'no':
            self.start()
        else:
            t_print("You do nothing and go down with the ship")
            t_print("Ending 5/5")

    """Section of the game in the left hall"""
    def left_hall(self):
        """Defines what is seen in the left hall"""
        t_print("\nYou run down the hall until you get to a wall")
        t_print("On the wall hangs a sign: ")
        t_print("       <- cafeteria")
        t_print("          escape pods -> ")
        t_print("        ^ control room")
        t_print("You can either go left to the cafeteria, right to the escape pods or back to the control room")
        choice_left = input("Where do you go(right or back): ").lower().strip()
        self.lefthall_choice(choice_left)
    
    def lefthall_choice(self, choice):
        """Evaluates the choice you make in the left hall"""
        if choice == 'back':
            self.right_hall()
        elif choice == 'right':
            self.escape()
        elif choice == 'left':
            self.cafe()
        else:
            t_print("\nYou do nothing and go down with the ship")
            t_print("Ending 5/5")
    
    def cafe(self):
        """Plays the cafeteria scenario"""
        Cafeteria()
        self.left_hall()

    """Section of the game in the left hall"""
    def right_hall(self):
        """Defines what is seen in the right hall"""
        t_print("\nYou run down the hall, while the other control room staff run past you in a blind panic")
        t_print("Finally you get to a locked door, above it is a sign with: ")
        t_print("                      'CONTROL ROOM'")
        t_print("There is a keypad next to the door to open it")
        t_print("You can either try to open the door or go back to see what is down the other hall")
        choice_right = input("What will you do(open or back): ").lower().strip()
        self.righthall_choice(choice_right)
    
    def righthall_choice(self, choice):
        """Evaluates the choice made in the right hall"""
        if choice == 'back':
            self.left_hall()
        elif choice == 'open':
            self.keypad()
        else:
            t_print("\nYou do nothing and go down with the ship")
            t_print("Ending 5/5")
    

    """Section of the game at the escape pods"""
    def escape(self):
        """Defines what happens if you go to the escape pods"""
        t_print("\nYou get to the hall with the escape pods, it's absolute mayhem")
        t_print("You notice that there are not nearly enough pods to help everyone of the ship")
        t_print("And anyone who's here runs to an empty pod, pushing everyone out of their way")
        t_print("Do you want to get in a pod and leave everyone to fend for themselves?")
        t_print("Or do you go back and attempt to get to the control room?")
        choice_escape = input("What will you do(escape or back): ").lower().strip()
        self.escape_choice(choice_escape)
    
    def escape_choice(self, choice):
        """Evaluates the choice to escape or not"""
        if choice == 'back':
            self.right_hall()
        elif choice == 'escape':
            self.escape_ending()
    
    def escape_ending(self):
        """Defines the escape ending"""
        t_print("\nYou see an empty pod not to far from you")
        t_print("Running towards it you shove a couple of colleagues aside")
        t_print("\nYou get into the escape pod and look back a final time")
        t_print("As you are launched into space there is only one thing to cross your mind: ")
        t_print("            How do I fly this thing?")
        t_print("Ending 4/5")
    

    """Section of the game at the control room entrance"""
    def keypad(self):
        """Defines the first puzzle at the keypad"""
        Puzzle1()

        code = input("Input your code here: ")
        self.code_evaluation(code)

    def code_evaluation(self, code):
        """Evaluates your answer to the puzzle"""
        if code == '6050':
            self.controlroom()
        else:
            self.retry()
    
    def retry(self):
        """Gives the player a second chance to solve the puzzle"""
        t_print("Wrong code; Try again")
        t_print("Hint: The code is: RADEC")
        code_retry = input("Input your code here: ")
        self.code_retry(code_retry)
    
    def code_retry(self, code):
        """Evaluates the second try"""
        if code == '6050':
            self.controlroom()
        else:
            self.failed()

    def failed(self):
        """Defines the failed keypad ending"""
        t_print("ALARM! ALARM! SHIP GOING DOWN")
        t_print("As you fail the code a second time the ship shudders")
        t_print("You lose your balance and fall to the ground")
        t_print("The final thing you see is flames erupting at the end of the hall")
        t_print("As your vision fades")
        t_print("Ending 2/5")


    """Section of the game in the control room"""
    def controlroom(self):
        """Defines what you see when you get into the control room"""
        t_print("When you enter the code, the light on the keypad turns green")
        t_print("ACCES GRANTED")
        t_print("You run into the control room and grab hold of the main console")
        t_print("As you look through the main window, you're taken aback")
        t_print("There doesn't seem to be anything out of the ordinary")
        t_print("You look down at the console and see that there is a warning sign flashing")
        t_print("WARNING: SHIP'S ORBIT COMPROMISED")
        t_print("RESET SYSTEM")
        t_print("You look around to figure out what you can do to reset the system")
        t_print("When you look around you see four stations, each flashing red") 
        t_print("You conclude that you have to reset all four stations to reset the system")

        Stations()

        choice_station = input("Which station do you want to reset first(1, 2, 3 or 4): ")
        self.station_choice(choice_station)
    
    def station_choice(self, choice):
        """Evaluates and sends you to the station you choose"""
        if choice == '1':
            self.station_1()
        elif choice == '2':
            self.station_2()
        elif choice == '3':
            self.station_3()
        elif choice == '4':
            self.station_4()
        else:
            t_print("\nYou do nothing and go down with the ship")
            t_print("Ending 5/5")
    
    def failed_station(self):
        """Defines the failed station ending"""
        t_print("ERROR! ERROR! SYSTEM FAILURE")
        t_print("INITIATE SELF DESTRUCT")
        t_print("As you fail the code a second time the ship shudders")
        t_print("You lose your balance and fall to the ground")
        t_print("Then everything goes black as the ship explodes around you")
        t_print("Ending 3/5")

    def possible_stations(self):
        """Defines the choices for the stations you haven't reset yet"""
        if all(self.stations_reset.values()):
            self.final_ending()
        else:
            remaining = [i for i, j in self.stations_reset.items() if not j]
            t_print(f"You still have to reset the following stations: {', '.join(remaining)}")
            new_station = input(f"Which station do you want to go next({', '.join(remaining)}): ")
            self.station_choice(new_station)

    """Section of the game at station 1"""
    def station_1(self):
        """Defines the puzzle for station 1"""
        Puzzle2()

        code = input("Input your order here: ")
        self.station1_code_evaluation(code)
    
    def station1_code_evaluation(self, code):
        """Evaluates your answer to the puzzle"""
        if code == 'MVEMJSUN':
            t_print("STATION 1 RESET")
            t_print("You have successfully reset station 1, you can now move on to the next station")
            self.stations_reset['Station 1'] = True
            self.possible_stations()
        else:
            t_print("Wrong order; Try again")
            code_retry = input("Input your order here: ")
            self.station1_code_retry(code_retry)
    
    def station1_code_retry(self, code):
        """Gives the player a second chance to solve the puzzle and gives a hint"""
        if code == 'MVEMJSUN':
            t_print("STATION 1 RESET")
            t_print("You have successfully reset station 1, you can now move on to the next station")
            self.stations_reset['Station 1'] = True
            self.possible_stations()
        else:
            self.failed_station()


    """Sections for station 2"""
    def station_2(self):
        """Defines the puzzle for station 2"""
        Puzzle3()

        code = input("Input your peaks here: ")
        self.station2_code_evaluation(code)

    def station2_code_evaluation(self, code):
        """Evaluates your answer to the puzzle"""
        if code == '20457095':
            t_print("STATION 2 RESET")
            t_print("You have successfully reset station 2, you can now move on to the next station")
            self.stations_reset['Station 2'] = True
            self.possible_stations()
        else:
            t_print("Includes correct data; Try again")
            t_print("Hint: Round the peak locations to fives")
            code_retry = input("Input your peaks here: ")
            self.station2_code_retry(code_retry)
    
    def station2_code_retry(self, code):
        """Gives the player a second chance to solve the puzzle and gives a hint"""
        if code == '20457095':
            t_print("STATION 2 RESET")
            t_print("You have successfully reset station 2, you can now move on to the next station")
            self.stations_reset['Station 2'] = True
            self.possible_stations()
        else:
            self.failed_station()
    

    """Section of the game at station 3"""
    def station_3(self):
        """Defines the puzzle for station 3"""
        Puzzle4()

        code = input("Input classification here: ")
        self.station3_code_evaluation(code)
    
    def station3_code_evaluation(self, code):
        """Evaluates your answer to the puzzle"""
        if code == 'G-yellow-Main sequence':
            t_print("STATION 3 RESET")
            t_print("You have successfully reset station 3, you can now move on to the next station")
            self.stations_reset['Station 3'] = True
            self.possible_stations()
        else:
            t_print("Includes correct data; Try again")
            t_print("Hint: The Sun has a temperature between 5000 and 6500 K")
            code_retry = input("Input your peaks here: ")
            self.station3_code_retry(code_retry)
    
    def station3_code_retry(self, code):
        """Gives the player a second chance to solve the puzzle and gives a hint"""
        """Evaluates your answer to the puzzle"""
        if code == 'G-yellow-Main sequence':
            t_print("STATION 3 RESET")
            t_print("You have successfully reset station 3, you can now move on to the next station")
            self.stations_reset['Station 3'] = True
            self.possible_stations()
        else:
            self.failed_station()

    
    """Section of the game at station 4"""
    def station_4(self):
        """Defines the puzzle for station 4"""
        Puzzle5()

        Input = input("Input the name of the third constellation: ").lower().strip()
        self.constellation_evaluation(Input)

    def constellation_evaluation(self, Input):
        """Evaluates your answer to the puzzle"""
        if Input == 'pegasus':
            t_print("CONSTELLATION 3 CORRECT")
            t_print("You have successfully reset station 4, you can now move on to the next station")
            self.stations_reset['Station 4'] = True
            self.possible_stations()
        else:
            t_print("Wrong constellation; Try again")
            t_print("Hint: Named after a mythical creature from Greek mythology")
            Input_retry = input("Input the name of the first constellation: ").lower().strip()
            self.constellation1_retry(Input_retry)

    def constellation1_retry(self, Input):
        """Gives the player a second chance to solve the puzzle and gives a hint"""
        if Input == 'pegasus':
            t_print("CONSTELLATION 3 CORRECT")
            t_print("You have successfully reset station 4, you can now move on to the next station")
            self.stations_reset['Station 4'] = True
            self.possible_stations()
        else:
            self.failed_station()

    """"Final ending of the game"""
    def final_ending(self):
        """Defines the final ending of the game"""
        t_print("\nAs you reset the last station, you feel that the ship has stopped shaking")
        t_print("You walk back to the main console and check the status")
        t_print("STABILIZATION SUCCESSFUL")
        t_print("YOU DID IT! YOU SAVED THE SHIP!")
        t_print("Now you can finally relax and enjoy the view of space on your journey home")
        t_print("Ending 1/5")


game = Game()
game.start()

# %%




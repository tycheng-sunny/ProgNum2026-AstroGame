#!/usr/bin/env python
# coding: utf-8

# In[ ]:


print("Welcome to SWEET SAVIOUR!"
      "\nA story based astronomy game in which you are tasked to save the world."
      "\n\nRead the following introduction and instructions carefully."
      "\nOnce you've read it all, press enter to start the game."
      "\n\nINSTRUCTIONS:"
      "\nDuring the story's progression you will be presented with questions and dilemma's."
      "\nAnswer correctly or there might be consequences."
      "\n\nBACKSTORY:"
      "\nIn this story you are an astronomer."
      "\nYou enjoy reading books and learning about foreign languages."
      "\nYou have studied astronomy in your younger years and still have very fond memories of it ;)"
      "\nOne evening you are sitting on the couch in your living room when suddenly...")
input("\nPRESS ENTER TO START THE GAME")


# In[2]:


import time

choice1 = None
choice2 = None
choice3 = None
choice4 = None
choice5 = None
choice6 = None
choice7 = None
choice8 = None
choice9 = None
choicelast = None
choicefunc = None


TEXT_DELAY = 1.5  # adjust speed here

def slow_print(text):
    '''Used to slow down printing of text to make it feel more realistic and conversation like'''
    print(text)
    time.sleep(TEXT_DELAY)

def get_choice(prompt, valid_options):
    ''' Checks wether input choice is valid and if not returns options to choose from '''
    while True:
        try:
            choice = int(input(prompt))
            if choice in valid_options:
                return choice
            else:
                print(f"Invalid input. Choose from {valid_options}.")
        except ValueError:
            print("Please enter a number.")

def get_choice_secret(prompt, valid_options, secret_option=None):
    """
    Checks whether input choice is valid (including secret option).
    If invalid, only shows normal options (secret stays hidden).
    """
    while True:
        try:
            choice = int(input(prompt))

            # accept both normal and secret option
            if choice in valid_options or choice == secret_option:
                return choice

            print(f"Invalid input. Choose from {valid_options}.")

        except ValueError:
            print("Please enter a number.")

# STORY START
slow_print("*knock *knock")
slow_print("You:           Who is there?")
slow_print("Unknown:       FBI OPEN UP!")
slow_print("You get up from the couch and are about to open the door for the FBI agent when doubt creeps in.")

slow_print("\nWILL YOU OPEN?")
#present first choice: will you open the door or not
choice1 = get_choice("Type 1 for yes, 2 for no, 3 for I'm not sure: ", [1, 2, 3])

if choice1 == 1:  # YOU OPEN THE DOOR
    slow_print("\nYou:           *Slowly opens the door.")
    slow_print("               What can I do for you madam?")

    slow_print("\nFBI Agent:     You have been called upon to come work on a mission.")
    slow_print("               Do you accept any and all consequences and risks this mission might bring?")

    # choice with secret third option which makes you gain extra pre-knowledge
    choice2 = get_choice_secret("Type 1 for yes, 2 for no: ", [1, 2], 3)

    if choice2 == 1:
        slow_print("\nYou:           I accept.")
        slow_print("FBI Agent:     Very well then... Come with me.")
        slow_print("\nYou are taken to a car and before you know it you've been driving for 2 hours.")
        

    elif choice2 == 2:
        slow_print("\nYou:           No...")
        slow_print("FBI Agent:     Sorry? What do you mean no...")
        slow_print("You:           I do not think I am suitable for whatever you want me for.")
        slow_print("FBI Agent:     Then I'm afraid we'll have to take you with or without your permission...")
        slow_print("\nYou are forcefully taken to a car and before you know it you've been driving for 2 hours.")

    elif choice2 == 3:
        slow_print("\nYou have unlocked a secret path!")
        slow_print("You:           What does the mission entail?")
        slow_print("FBI Agent:     I can not tell you the full details...")
        slow_print("               What I can tell you is that this mission is of great importance to the safety of all of mankind.")
        slow_print("               We need an expert in the fields of linguistics and outer space")
        slow_print("               and heard that you might know a thing or two about that.")
        slow_print("               I'm afraid thats all the information I can share.")
        slow_print("               Will you accept and do you accept any and all consequences and risks this mission brings?")

        # Regive the choice to yes or no with the knew knowledge
        choice2 = get_choice("Type 1 for yes, 2 for no: ", [1, 2])

        if choice2 == 1:
            slow_print("\nYou:           I accept.")
            slow_print("FBI Agent:     Very well then... Come with me.")
            slow_print("\nYou are taken to a car and before you know it you've been driving for 2 hours.")

        elif choice2 == 2:
            slow_print("\nYou:           No...")
            slow_print("FBI Agent:     Sorry? What do you mean no...")
            slow_print("You:           I do not think I am suitable for whatever you want me for.")
            slow_print("FBI Agent:     Then I'm afraid I'll have to take you with or without your permission...")
            slow_print("\nYou are forcefully taken to a car and before you know it you've been driving for 2 hours.")


elif choice1 == 2:  # YOU DON'T OPEN THE DOOR
    slow_print("\nYour hand freezes right above the door handle.")
    slow_print("~ What could the FBI possibly want from me...? ~")
    slow_print("~ They will probably leave if I don't answer the door ~")
    slow_print("\nYou decide to go back to whatever you were doing before the fbi knocked.")
    slow_print("Through the window you see the FBI agent standing next to her car, nothing special...")
    slow_print("\nAfter a few minutes you realise there were never any other knocks or sounds.")
    slow_print("~ I guess it was not as urgent after all. ~")
    choice3=2
    


elif choice1 == 3:  # YOU DON'T OPEN THE DOOR YET
    slow_print("\nYou are not sure wether to open the door or not...")
    slow_print("~ What could the FBI possibly want from me...? ~")
    slow_print("You decide to walk to the window to investigate before opening the door.")
    slow_print("When you look out of the window you see a woman standing next to a large black car with tinted windows.")
    slow_print("She says something through her walkietalkie.")
    slow_print("Through the crack in the open window you can just hear what she says.")
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\nFBI Agent:     Agent 42 here...")
    slow_print("Other line:    ###* incomprehensible crackling #*##")
    slow_print("FBI Agent:     Unfortunately not, we will have to find another expert to help us deal with our extraterrestrial issue.")
    slow_print("Other line:    *#**## More crackling noise ##*#")
    slow_print("               #*## Humanity #*## extinct ##**# find *##*# quickly **##*#*")
    slow_print("FBI Agent:     I'll look into it. I'm heading back to the station now so I'll see you there.")

    slow_print("\nAfter hearing the conversation between the FBI Agent and their coworker you start to doubt your decision to not open the door.")

    slow_print("\nWILL YOU QUICKLY OPEN THE DOOR AND GO AFTER THE FBI AGENT?")

    # Give the choice to go after the agent or not
    choice3 = get_choice("Type 1 for yes, 2 for no: ", [1, 2])

    if choice3 == 1:
        slow_print("\nYou decide to quickly go after the FBI agent hoping to make up for not opening the door.")
        slow_print("While unlocking the door you quickly try to find an excuse for ignoring the FBI agents knocks.")
        slow_print("Luckily the FBI agent is still outside her car, focused on her phone.")
        slow_print("You:           Hello! I'm so sorry I thought some kids were pranking me.")
        slow_print("FBI Agent:     Oh thank god, I was afraid id have to find someone else.")
        slow_print("You:           To do what exactly?")
        slow_print("You:           I didn't mean to eavesdrop but I overheard you talking about needing an expert?")
        input("\nPRESS ENTER TO CONTINUE")
        slow_print("\nFBI Agent:     I unfortunately can't share much, but you are correct.")
        slow_print("               I knocked on your door because you have been called upon to come work on a mission.")
        slow_print("               What I can tell you is that this mission is of great importance to the safety of all of mankind.")
        slow_print("               We need an expert in the fields of linguistics and outer space")
        slow_print("               and heard that you might know a thing or two about that.")
        slow_print("               I'm afraid thats all the information I can share.")
        slow_print("               Will you accept and do you accept any and all consequences and risks this mission brings?")

        # Regive choice 2, go willingly or not
        choice2 = get_choice("Type 1 for yes, 2 for no: ", [1, 2])

        if choice2 == 1:
            slow_print("\nYou:           I accept.")
            slow_print("FBI Agent:     Very well then... Come with me.")
            slow_print("\nYou are taken to a car and before you know it you've been driving for 2 hours.")

        elif choice2 == 2:
            slow_print("\nYou:           No...")
            slow_print("FBI Agent:     Sorry? What do you mean no...")
            slow_print("You:           I do not think I am suitable for whatever you want me for.")
            slow_print("FBI Agent:     Then I'm afraid I'll have to take you with or without your permission...")
            slow_print("\nYou are forcefully taken to a car and before you know it you've been driving for 2 hours.")
            slow_print("~ I should've just stayed inside... why did I open the door. ~")

    elif choice3 == 2:
        slow_print("\nYou decide that it's probably the best option to stay inside and let the FBI find a new 'expert'.")
        slow_print("~ Whatever that may mean... ~")
        slow_print("After a few minutes you realise there were never any other knocks or sounds.")
        slow_print("~ I guess it was not as urgent after all. ~")
        choice1=2


# In[ ]:


''' TRACK 1 INEVITABLE DOOM '''
''' CHOSE NOT TO OPEN DOOR AT ALL WHICH LEADS TO THE FALL OF ALL OF MANKIND '''


if choice1 == 2:
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\nThree weeks go by since the strange knocks on your door from the FBI.")
    slow_print("The memory of it was nearly faded fully untill now...")
    slow_print("You stare at the television on which the evening news is shown.")
    slow_print("Same as always... Except for the fact that its not.")
    slow_print("\nOn the screen you see footage from New York, Paris, Athens, Tokyo and about 10 other mayor cities in the world.")
    slow_print("All cities look like they always do, except there are no people.")
    slow_print("It is all empty.")
    slow_print("\nThe screen switches to a reporter who seems to be interviewing an FBI agent just outside of New York.")
    slow_print("Then the agent turns around...")
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\n~ It's her.. ~")

    slow_print("~ The agent from that night.. ~")
    slow_print("~ That can't be her right ~")
    slow_print("~ No.. It's definitely her ~")
    slow_print("~ What if she was at my house for a reason? ~")

    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\nReporter:      What is going on here?! Please tell us!")
    slow_print("FBI Agent:     Aliens have invaded planet earth.")
    slow_print("               Over the last couple of weeks we have tried to communicate with them.")
    slow_print("               Unfortunately we could not understand their language, and we believe they could not understand us either.")
    slow_print("               We tried to find linguistic experts who could.......")
    slow_print("\n~ NO ~")
    slow_print("~ PLEASE TELL ME THIS IS NOT HAPPENING ~")
    slow_print("\nFBI Agent:    ...... All experts were unavailable or could not be tracked down.")
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\n~ IT IS ALL MY FAULT... ~")
    slow_print("~ IF I HAD JUST OPENED THE DOOR, NONE OF THIS WOULD BE HAPPENING ~")
    slow_print("~ I HAVE DOOMED HUMANITY ~")
    slow_print("\nReporter:      You heard her.")
    slow_print("               Everyone stay inside, lock your doors, and do not come out untill the alien creatures have left...")
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\n....")
    slow_print("Weeks pass.")
    slow_print("...")
    slow_print("After 20 weeks nearly all humans on earth have mysteriously dissapeared.")
    slow_print("Noone knows why, how, or where to.")
    slow_print("All that is known is that the creatures that invaded our home are staying here for good.")

    TEXT_DELAY = 0
    slow_print("\n----------------------------------------------------------")
    slow_print(" YOU HAVE COMPLETED THE GAME THROUGH TRACK 1: INEVITABLE DOOM ")
    slow_print(" TO EXPLORE OTHER TRACKS YOU CAN RESTART THE GAME AND MAKE OTHER CHOICES!")
    TEXT_DELAY = 1.5

    


# In[ ]:


''' TRACK 2 EARTH CAN BE SAVED'''
''' ESCORT INSIDE THE FACILITY'''


''' WILLING PATH'''
''' WITHOUT KNOWLEDGE'''
if choice1==1 and choice2==1:
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\nAfter the long journey you finally arrive at the destination.")
    slow_print("The FBI Agent 42 escorts you inside.")
    slow_print("Your mind goes blank as the security searches you and asks for your identification and any other personal belongings.")
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\nEveryone is rather nice and chill, but there is still an eery atmosphere.")
    slow_print("After everything is 'secure', according to the guards,")
    slow_print("you are led to a room that looks an awfull lot like an interrogation room from movies.")
    slow_print("FBI Agent:     Don't worry too much, all will be explained shortly.")
    choice4=1
    
''' WITH KNOWLEDGE'''
if choice1==3 and choice3==1 and choice2==1:
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\nAfter the long journey you finally arrive at the destination.")
    slow_print("On the drive Agent 42 assures you everything will be allright, which calms your nerves slightly.")
    slow_print("Then the agent escorts you inside.")
    slow_print("Your mind goes blank as the security searches you and asks for your identification and any other personal belongings.")
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\nEveryone is rather nice and chill, but there is still an eery atmosphere.")
    slow_print("After everything is 'secure', according to the guards,")
    slow_print("you are led to a room that looks an awfull lot like an interrogation room from movies.")
    slow_print("FBI Agent:     Don't worry too much, all will be explained shortly.")
    choice4=2

''' FORCED PATH'''
''' WITHOUT KNOWLEDGE '''
if choice1==1 and choice2==2:
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\nAfter the long journey you finally arrive at the destination.")
    slow_print("The FBI Agent 42 escorts you inside.")
    slow_print("You try to resist but the agent and security around the building are clearly stronger.")
    slow_print("Your mind goes blank as the security searches you and asks for your identification and any other personal belongings.")
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\nGuard:         Hey, answer our questions clearly and quickly!")
    slow_print("\nThere is an eery and dark atmosphere around that makes you even more stressed.")
    slow_print("I never wanted to be here in the first place.")
    slow_print("After everything is 'secure', according to the guards,")
    slow_print("you are led to a room that looks an awfull lot like an interrogation room from movies.")
    slow_print("FBI Agent:     Sit tight and all will be explained shortly.")
    choice4=1

''' WITH KNOWLEDGE '''
if choice1==3 and choice3==1 and choice2==2:
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\nAfter the long journey you finally arrive at the destination.")
    slow_print("The FBI Agent 42 escorts you inside.")
    slow_print("You try to resist but the agent and security around the building are clearly stronger.")
    slow_print("Your mind goes blank as the security searches you and asks for your identification and any other personal belongings.")
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\nGuard:         Hey, answer our questions clearly and quickly!")
    slow_print("\nThere is an eery and dark atmosphere around that makes you even more stressed.")
    slow_print("I never wanted to be here in the first place.")
    slow_print("After everything is 'secure', according to the guards,")
    slow_print("you are led to a room that looks an awfull lot like an interrogation room from movies.")
    slow_print("FBI Agent:     Sit tight and all will be explained shortly.")
    choice4=2


# In[4]:


''' MISSION EXPLANAITION '''
'''WITHOUT PRIOR KNOWLEDGE'''
if choice4 == 1:
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\nFBI Agent:     You are now part of a secret mission whether you like it or not.")
    slow_print("               This is not public news yet, and we'd like to keep it that way until we know how it will play out.")

    slow_print("You:           What do you mean? What is going on?")

    slow_print("FBI Agent:     Creatures from another world have invaded our planet.")
    slow_print("               We believe they are here for some purpose, but we have yet to figure out what this purpose is.")
    slow_print("               Which is where you come in.")
    slow_print("\nYou:           What could I possibly do for you that you can't get from anyone else?")
    input("\nPRESS ENTER TO CONTINUE")

    slow_print("\nFBI Agent:     You are an astronomer and have also shown interest in foreign and dead languages...")
    slow_print("               Am I correct about that?")

    slow_print("\nYou:           Yes, I guess I've developed an interest in languages over the years.")

    slow_print("FBI Agent:     Alright then, you have answered your own question.")
    slow_print("               We need both of those fields, astronomy and linguistics,")
    slow_print("               to decipher what the alien creatures are trying to tell us.")
    slow_print("               You are perfect for this task due to a number of other reasons too.")
    slow_print("               The aliens seem to have taken a dislike to men,")
    slow_print("               and since there are not many women in the fields of astronomy and physics, our options were limited.")

    slow_print("You:           I see...")

    slow_print("FBI Agent:     I hope you will offer your experience and knowledge to help us save humanity.")

    slow_print("\nYou:           I guess I will help.")

    slow_print("FBI Agent:     Great, come with me.")
    choice5 = 1
    

'''WITH PRIOR KNOWLEDGE'''
if choice4 == 2:
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\nFBI Agent:     As Agent 42 has already explained, you are now part of a secret mission.")
    slow_print("               This is not public news yet, and we'd like to keep it that way until we know how it will play out.")

    slow_print("FBI Agent:     Creatures from another world have invaded our planet.")
    slow_print("               We believe they are here for some purpose, but we have yet to figure out what this purpose is.")
    slow_print("               Which is where you come in.")
    slow_print("               What could I possibly do for you that you can't get from anyone else?")
    input("\nPRESS ENTER TO CONTINUE")

    slow_print("\nFBI Agent:     You are an astronomer and have also shown interest in foreign languages...")
    slow_print("               Am I correct about that?")

    slow_print("You:           Yes, I guess I've developed an interest in languages over the years.")

    slow_print("FBI Agent:     Alright then, you have answered your own question.")
    slow_print("               We need both of those fields, astronomy and linguistics,")
    slow_print("               to decipher what the alien creatures are trying to tell us.")
    slow_print("               You are perfect for this task due to a number of other reasons too.")
    slow_print("               The aliens seem to have taken a dislike to men,")
    slow_print("               and since there are not many women in the fields of astronomy and physics, our options were limited.")

    slow_print("\nYou:           I see...")

    slow_print("FBI Agent:     I hope you will offer your experience and knowledge to help us save humanity.")

    slow_print("\nYou:           I guess I will help.")

    slow_print("FBI Agent:     Great, come with me.")
    choice5 = 1
    


# In[ ]:


''' EXTRA INFO ABOUT MISSION '''
if choice5 == 1:
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\nThe fbi agent explained everything to you.")
    slow_print("The aliens speak in a language we can't decipher.")
    slow_print("It's just a blur of letters.")
    slow_print("\nThere are a few things about the creatures that caught your attention.")
    slow_print("Firstly there are symbols on the side of the space ship:")
    slow_print("\n /-/ |_| |3 |3 |_ |≡ ")
    input("\nPRESS ENTER TO CONTINUE")
    
    slow_print("\nThe spaceship they arrived in contained data that you very clearly recognise.")
    slow_print("In your study years at university you used this exact type of data to get physical constants.")
    slow_print("\n~ What if the data will lead to a constant that we can use to decipher their language ~")
    slow_print("~ It's worth a try, so why not do it ~")
    slow_print("You decide to upload the data to your computer and try and extract a constant.")
    choice6 = 1


# In[ ]:


''' CHOOSE CORRECT TABLES AND CONSTANT SO YOU CALCULATE THE RIGHT THING '''
''' CHECK EACH OPTION TO SEE IF INPUT IS FULLY VALID OR NOT '''
if choice6 == 1:
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\nYou write the code to extract the correct data from the alien spaceship.")
    slow_print("You find that there are multiple tables in the data.")
    slow_print("\nThe tables found in the data have the following names:")
    slow_print("---Force, Redshift, Frequency, Length, Mass, Intensity, Volume, Magnitude, Viscosity---")
    
    allowed_tables = {"mass","frequency","redshift","volume","viscosity","magnitude","intensity","force","length"}

    slow_print("You assume only two of these tables are needed for the constant calculation.")
    slow_print("\nThere are a few constants you know of.")
    slow_print("---Magnetic permeability, Speed of light, Hubble constant, Pi, Avogadro---")
    
    input("\nPRESS ENTER TO CONTINUE")
    
    allowed_constants = {"magnetic permeability","speed of light","hubble constant","pi","avogadro"}
    
    slow_print("\nWhich of these constants are you most likely to find in the data?")
    while True:
        choice7 = input("Type the name of the constant you wish to try and calculate: ")

        # normalise input (case-insensitive + remove extra spaces)
        normalized_choice = choice7.strip().lower()

        if normalized_choice in allowed_constants:
            break
        else:
            print("Invalid choice. Please select one of the listed constants.")
        
    slow_print("\nNow that you have chosen a constant,")
    slow_print("you have to decide which tables from the data you will pick?")
    # ---- choice 8 ----
    while True:
        choice8 = input("Type the name of the first table header you wish to use: ")
        choice8_norm = choice8.strip().lower()

        if choice8_norm in allowed_tables:
            break
        else:
            print("Invalid table name. Please choose from the listed tables.")

    # ---- choice 9 ----
    while True:
        choice9 = input("Type the name of the second table header you wish to use: ")
        choice9_norm = choice9.strip().lower()

        if choice9_norm not in allowed_tables:
            print("Invalid table name. Please choose from the listed tables.")
        elif choice9_norm == choice8_norm:
            print("You cannot select the same table twice. Please choose a different one.")
        else:
            break


# In[ ]:


''' FINAL RESULTS BASED ON WHAT TABLE AND CONSTANT YOU PICKED'''

while True:

    choice7_norm = choice7.strip().lower()
    choice8_norm = choice8.strip().lower()
    choice9_norm = choice9.strip().lower()

    valid_pair = {choice8_norm, choice9_norm}

    if (
        choice7_norm == "hubble constant"
        and valid_pair == {"redshift", "magnitude"}
    ):
        print("You have selected the Hubble constant, redshift, and magnitude.")
        choicelast = 1
        break

    else:
        print("You've selected your constant and tables.")
        choicelast = 2
        break


if choicelast == 2:
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\nWith your selected constants you try to calculate a constant.")
    slow_print("After days of work you have still not gotten any value which lead to a clear deciphering of the alien language.")
    slow_print("After two weeks you still have not gotten any results.")
    slow_print("That is when the alarm at the secret facility goes off...")
    
    input("\nPRESS ENTER TO CONTINUE")
    
    slow_print("\n * ALERT * ")
    slow_print("The alien creatures have escaped. ")
    slow_print("There is full chaos in all rooms.")
    slow_print("Then everything goes quiet.")
    input("\nPRESS ENTER TO CONTINUE")
    
    slow_print("\nThe evening news is on in many homes around the world.")
    slow_print("Same as always... Except for the fact that its not.")
    slow_print("\nOn the screen footage from New York, Paris, Athens, Tokyo and about 10 other mayor cities in the world is shown.")
    slow_print("All cities look like they always do, except there are no people.")
    slow_print("It is all empty.")
    
    input("\nPRESS ENTER TO CONTINUE")
    
    slow_print("\nThe screen switches to a reporter who seems to be interviewing an FBI agent just outside of New York.")
    slow_print("Reporter:      What is going on here?! Please tell us!")
    slow_print("FBI Agent:     Aliens have invaded planet earth.")
    slow_print("               Over the last couple of weeks we have tried to communicate with them.")
    slow_print("               We tried for weeks to decipher the creatures language..")
    slow_print("               Unfortunately with no result.")
    slow_print("               The creatures have taken control and we don't know how to stop them.")
    
    input("\nPRESS ENTER TO CONTINUE")
    
    slow_print("\nWeeks pass.")
    slow_print("...")
    slow_print("After 20 weeks nearly all humans on earth have mysteriously dissapeared.")
    slow_print("Noone knows why, how, or where to.")
    slow_print("All that is known is that the creatures that invaded our home are staying here for good.")

    TEXT_DELAY = 0
    slow_print("\n----------------------------------------------------------")
    slow_print(" YOU HAVE COMPLETED THE GAME THROUGH TRACK 2: FAILED ATTEMPT")
    slow_print(" TO EXPLORE OTHER TRACKS YOU CAN RESTART THE GAME AND MAKE OTHER CHOICES!")
    TEXT_DELAY = 1.5


if choicelast == 1:
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("To calculate Hubble's constant you have extracted the tables for redshift and the magnitude.")
    slow_print("However you know you need the velocity and not the reshift.")
    slow_print("Which of the following options is the correct way of calculating the velocity.")
    slow_print("\nOption 1: v = c/z"
               "\nOption 2: v = c*z"
               "\nOption 3: v = c**z")

    choicefunc = get_choice("Type 1 for option 1, 2 for option 2, 3 for option 3: ", [1, 2, 3])

    if choicefunc == 1 or choicefunc == 3:
        slow_print("\nYou fill in the equation and try to find a constant.")
        slow_print("After days of work you have still not gotten any value which lead to a clear deciphering of the alien language.")
        slow_print("After two weeks you still have not gotten any results.")
        slow_print("That is when the alarm at the secret facility goes off.")
        
        input("\nPRESS ENTER TO CONTINUE")
        slow_print("\n * ALERT * ")
        slow_print("The alien creatures have escaped.")
        slow_print("There is full chaos in all rooms.")
        slow_print("Then everything goes quiet.")
        input("\nPRESS ENTER TO CONTINUE")
        slow_print("\nThe evening news is on in many homes around the world.")
        slow_print("Same as always... Except for the fact that its not.")
        slow_print("\nOn the screen footage from New York, Paris, Athens, Tokyo and about 10 other mayor cities in the world is shown.")
        slow_print("All cities look like they always do, except there are no people.")
        slow_print("It is all empty.")
        
        input("\nPRESS ENTER TO CONTINUE")
        
        slow_print("\nThe screen switches to a reporter who seems to be interviewing an FBI agent just outside of New York.")
        slow_print("Reporter:      What is going on here?! Please tell us!")
        slow_print("FBI Agent:     Aliens have invaded planet earth.")
        slow_print("               Over the last couple of weeks we have tried to communicate with them.")
        slow_print("               We tried for weeks to decipher the creatures language..")
        slow_print("               Unfortunately with no result.")
        slow_print("               The creatures have taken control and we don't know how to stop them.")

        input("\nPRESS ENTER TO CONTINUE")
        
        slow_print("Weeks pass.")
        slow_print("...")
        slow_print("After 20 weeks nearly all humans on earth have mysteriously dissapeared.")
        slow_print("Noone knows why, how, or where to.")
        slow_print("All that is known is that the creatures that invaded our home are staying here for good.")
        
        TEXT_DELAY = 0
        slow_print("\n----------------------------------------------------------")
        slow_print(" YOU HAVE COMPLETED THE GAME THROUGH TRACK 2: FAILED ATTEMPT")
        slow_print(" TO EXPLORE OTHER TRACKS YOU CAN RESTART THE GAME AND MAKE OTHER CHOICES!")
        TEXT_DELAY = 1.5


import numpy as np
import matplotlib.pyplot as plt
from astroquery.sdss import SDSS


class HubblePlotter:
    ''' Class for importing and handling for the hubble constant calculation and plotting'''
    def __init__(self):
        self.z = None
        self.m = None
        self.v = None
        self.d = None
        self.H0 = None

    def load_data(self):
        ''' Create a query and search for the needed items in SDSS'''
        query = """
        SELECT TOP 1000
            s.z,
            p.modelMag_r
        FROM SpecObjAll s
        JOIN PhotoObjAll p ON s.bestObjID = p.objID
        WHERE
            s.z BETWEEN 0.01 AND 0.5
            AND p.modelMag_r BETWEEN 14 AND 20
        """

        res = SDSS.query_sql(query, data_release=17, timeout=60)

        if res is None:
            raise RuntimeError("SDSS query failed or returned no data")

        self.z = np.array(res['z'])
        self.m = np.array(res['modelMag_r'])

    def compute(self):
        ''' Calculate the hubble constant with the found values '''
        c = 3e5
        M = -21

        # velocity from redshift
        self.v = c * self.z

        # distance modulus
        d_pc = 10 ** ((self.m - M + 5) / 5)
        self.d = d_pc / 1e6  # convert to Mpc

        # Hubble constant fit
        coef = np.polyfit(self.d, self.v, 1)
        self.H0 = coef[0]

    def plot(self):
        ''' Plot the hubble constant to check if it is indeed hubble '''
        plt.figure()

        plt.scatter(self.d, self.v, s=5, alpha=0.5)

        fit_line = self.H0 * self.d
        plt.plot(self.d, fit_line)

        plt.xlabel("Distance (Mpc)")
        plt.ylabel("Velocity (km/s)")
        plt.title(f"Hubble Law Fit (H0 ≈ {self.H0:.2f})")

        plt.show()

    def run(self):
        ''' What to print if everything is calculated and plotted'''
        slow_print("\nYou calculate the velocity using the chosen equation")

        self.load_data()
        self.compute()

        slow_print(f"Finally after days of work you found: {self.H0:.2f}")
        slow_print("This is close to Hubble's constant...")
        slow_print("To check wether it is indeed Hubble's constant,")
        slow_print("or at least a value close to it,")
        slow_print("you decide to plot it")
        

        self.plot()


# Run the hubbleplotter class to get the value needed for the translation
if choicefunc == 2:
    input("\nPRESS ENTER TO CONTINUE")
    runner = HubblePlotter()
    runner.run()
    slow_print("\n~ That looks really similar to what I remember it should look like! ~")
    slow_print("~ That must mean the constant means something to these creatures ~")
    slow_print("FBI Agent: *Somewhere on the background talking to another agent")
    slow_print("           I don't know man, to me it looked like one of those childhood diaries.")
    slow_print("           Like the ones where you make each letter another letter in the alphabet")
    slow_print("           by moving the alphabet over a few spots")
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\n~ Wow, how did I not think of that! ~")
    slow_print("~ I used to do those puzzles all the time as a kid... ~")
    slow_print("You quickly write down the alphabet on two strips of paper")
    slow_print("~ Could it be Hubbles constant? ~")
    slow_print("~ I might aswell try it ~")
    input("\nPRESS ENTER TO CONTINUE")
    slow_print("\nYou grab the written down alien language")
    slow_print("ck nkgxj znkxk oy igtje ut znoy vrgtkz, ck cuarj roqk yusk."
               "5 inuiurgzky corr ju. ol ck jutz mkz oz lxus eua ck corr ngbk"
               "zu lotj yuskutk cnu grcgey ngy igtje gtj ck cut'z yzuv atzorr"
               "ck lotj znks")
    slow_print("You decipher the code using a transfer of 6, which is the first digit of the found Hubble constant")
    input("\nPress Enter to continue once you've decoded the language...")
    slow_print("\n~ They want candy... ~")
    slow_print("~ Thats it... ~")
    slow_print("You:          GUYS GUYS GUYS")
    slow_print("              ALL THEY WANT IS CHOCOLATE")
    slow_print("              GIVE THEM CHOCOLATE")
    slow_print("\nTo be sure of humanities survival 5 trucks full of candy and chocolate are given to the creatures")
    slow_print("They happily leave earth and return to their homeplanet")
    TEXT_DELAY = 0
    slow_print("\n----------------------------------------------------------")
    slow_print(" YOU HAVE COMPLETED THE GAME THROUGH TRACK 3: SWEET SAVIOUR")
    slow_print(" TO EXPLORE OTHER TRACKS YOU CAN RESTART THE GAME AND MAKE OTHER CHOICES!")
    TEXT_DELAY = 1.5
    


# In[ ]:





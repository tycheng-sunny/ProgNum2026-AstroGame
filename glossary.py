"""
GAMES: game registry -- display name: path
AUTHOR_NAMES: game creator
"""

GAMES = {
    "Alien Dress-up Game": "game-NK/",
    "Asteroid Game": "game-DAC/",
    "Astronomy Constellation Quiz": "game-AT/",
    "Astroscanner": "game-AP/",
    "Astro Quiz": "game-IM",
    "Big Bang Odyssey": "game-GP",
    "Black Hole Game": "game-SL/",
    "Colour Matcher": "game-MG/",
    "Constellations Quiz": "game-VCT/",
    "Constellation Guessing Game": "game-JW/",
    "Cosmic Deal or No Deal": "game-MR",
    "Exoplanet Game": "game-HG/",
    "Galactic Golf": "game-JA/",
    "Galactic Shooter": "game-NS.",
    "Galaxy Finder": "game-AVP",
    "Galaxy Matcher": "game-BD/",
    "Gambling Game": "game-KG/",
    "GeoGuesser": "game-BC/",
    "HorizonScape": "game-EB/",
    "Intergalactic Travel": "game-AHH/",
    "Ionise HI Clouds": "game-AH",
    "Management Sim": "game-LBB/",
    "Medicine across the Universe": "game-LS/",
    "Memorising Galaxies": "game-LK/",
    "New Home": "game-SH/",
    "Planet Explorer": "game-BF/",
    "Puzzle Game": "game-AS/",
    "Save the Ship": "game-MB/",
    "Solar System Memory Game": "game-SEH/",
    "Sombrero": "game-OA/",
    "Space Invaders": "game-ML/",
    "Space Rescue Game": "game-ND/",
    "Spaceworm": "game-TB/",
    "Star Explorer": "game-IF/",
    "Star Wars": "game-SK/",
    "Stellar Evolution Simulator": "game-GK/",
    "Sunglasses in Space": "game-SA/",
    "Sweet Saviour": "game-AV/",
    "The Planet Defender": "game-SB",
    "Tim Shooter Game": "game-YM",
    "Travel to Exoplanet": "game-LJ/",
    "Virtual Telescope Project": "game-BB/",
    "Voyage": "game-MDB",
}

AUTHOR_NAMES = {
    "Alien Dress-up Game": "N. Krosse",
    "Asteroid Game": "D. Alvarez Corres",
    "Astronomy Constellation Quiz": "A. Tarzian",
    "Astroscanner": "A. Pafitis",
    "Astro Quiz": "I. Mazzei Braschi",
    "Big Bang Odyssey": "G. Parra San Pedro",
    "Black Hole Game": "S. Leszek",
    "Colour Matcher": "M. Gerritsen",
    "Constellations Quiz": "V. Calvo Tenza",
    "Constellation Guessing Game": "J. Whibley",
    "Cosmic Deal or No Deal": "M. Rosberg",
    "Exoplanet Game": "H. Atela Gonzalez",
    "Galactic Golf": "J. Alberda",
    "Galactic Shooter": "N. Stephen",
    "Galaxy Finder": "A. Valmana Perez",
    "Galaxy Matcher": "B. Dobak",
    "Gambling Game": "K. Godzieba",
    "GeoGuesser": "B. Chylinska",
    "HorizonScape": "E. Bartucz",
    "Intergalactic Travel": "A. Hofman",
    "Ionise HI Clouds": "A. Hreniuc",
    "Management Sim": "L. Burgos Ballester",
    "Medicine across the Universe": "L. Suberbere",
    "Memorising Galaxies": "L. Klingens",
    "New Home": "S. Haag",
    "Planet Explorer": "B. Flikkema",
    "Puzzle Game": "A. Stroeve",
    "Save the Ship": "M. Boer",
    "Solar System Memory Game": "S. Huijbers",
    "Sombrero": "O. Assenberg",
    "Space Invaders": "M. Lavik",
    "Space Rescue Game": "N. Demmenie", 
    "Spaceworm": "T. Balvin",
    "Star Explorer": "I. Frank",
    "Star Wars": "S. Kokkola",
    "Stellar Evolution Simulator": "G. Ketchum",
    "Sunglasses in Space": "S. Arentsen",
    "Sweet Saviour": "A. Vecht",
    "The Planet Defender": "S. Bazigos",
    "Tim Shooter Game": "Y. Mesu",
    "Travel to Exoplanet": "L. Jawinski",
    "Virtual Telescope Project": "B. Balas",
    "Voyage": "M. Bakelaar",
}

GAME_INFO = {
    "Alien Dress-up Game": "Make your alien the most stylish lifeform in the quadrant! Swap hairstyles and outfits against the stunning backdrop of the M101 galaxy.",

    "Asteroid Game": "Collect belts while avoiding asteroids that reduce your health. The game ends when your health reaches 0.",

    "Astronomy Constellation Quiz": "Astronomy Constellation Quiz\n\n"
        "This game shows constellation images and asks the user to type their names. (First letter is capital.)\n\n"
        "Rules:\n\n    "
        "- 20 random questions from 31 constellations\n    "
        "- Case-sensitive answers\n    "
        "- 3 attempts per question\n    "
        "- \"SKIP\" skips the question\n    "
        "- Timer limits total game time\n\n"
        "Dataset: All astronomical images are taken from kaggle: https://www.kaggle.com/datasets/theprakharsrivastava/stargazer",

    "Astroscanner": "You are in a 11x11 galaxy and your goal is to scan correctly 3 stars to be sent home. You can move up, down, left and right and you will be notified when you find a star, after which you have to guess which star it is based on its temperature.",

    "Astro Quiz": "To play the game, you just input your name and start answering questions and learn about astronomy.",

    "Big Bang Odyssey": "You are the last human alive, far from home and with the only help of A.L.I the artificial intelligence of your ship. The fuel is running out, to earn some you will need to play poker hands and continue your trip, trying to avoid the extinction of the humanity. \n\n"
        "The game consist in a poker game, where you can play a total of 4 hands (5 cards each) and discard 3 times (5 cards again). You will need to get the best hands in order to win more points and pass to the next level.\n\n"
        "After each level, an astronomical question is asked, if your answer is right, you will earn more credits; if it is not, nothing will happen. This credits are useful to buy jokers and boosts that will help you during the game.It has 5 rounds, increasing the level of difficulty in each.\n\n"
        "NOTE: When playing multiple cards, type <space> between each index.",

    "Black Hole Game": "Game inspired by pacman - player uses arrow keys to steer their black hole and eat stars, gathering their mass. User can eat other black holes as long as their black hole has bigger mass. Other black holes are like ghosts in pacman - they can eat you! Win when user absorbs all black holes or stars, or has the most mass of all objects.",
    "Colour Matcher": "In this game, you need to get the same color values as given to you, at the upmost left corner there is a hue that you need to match. (here you can also see the percentage of pixels that are that color). Just move your mouse over the image to get values in the graph and get them inside the range. You can get a new color if this one is too hard or you cannot find it.",

    "Constellations Quiz": "Before playing this little quiz, make sure you are an astronomy lover, above all a constellations freak. Once you satisfy the most important condition, you can start playing it to challenge yourself on your stars knowledge. \n\n"
        "Instructions: \n "
        "1. You will be given a random main star of a constellation \n "
        "2. Try to guess the constellation to win points \n "
        "3. Once you guessed t correctly, you can see the constellation \n "
        "4. Then, repeat until you have learnt all of them \n\n"
        "Good luck guessing and have fun!",

    "Constellation Guessing Game": "Follow the instructions to guess which constellation is being shown!\n\n"
        "[yellow]IMPORTANT NOTE: While the game itself is functional and fun to play, the intended final result cannot be fully presented because the image folder required by the game was not provided by the creator.[/yellow]",

    "Cosmic Deal or No Deal": "COSMIC DEAL OR NO DEAL\n\n    "
        "A classic game of Deal or No Deal; however with a cosmic twist. Instead of trying to earn as much money as possible, the goal is to get the highest amount of mass possible.\n\n    "
        "First, you select a case you will keep until the end and the premise is to open cases, hoping that the cases contain low-mass objects. Every 3 rounds, the banker calls, offering you a certain amount of mass. It's your choice if you accept it (Deal) or not (No Deal). The game ends either by taking a deal from the banker or until the final case is opened, revealing what case you have.\n\n"
        "HOW TO PLAY\n\n    "
        "The game is very simple to play. First you select a number from 0-9, typing it into the command line. Once the case is selected, you are shown a list of numbers you still haven't selected/opened. These cases can be opened by typing one of the remaining numbers from the list. (This list updates every time a case is opened, so no need to worry about losing track of what cases were opened already.)\n\n    "
        "Once the banker calls, you can either type \"deal\" or \"no\" depending on if you accept the Deal or not. This depends on how much you want to risk or how much the dealer offers. To make sure the person knows the items they're playing for, a list of cosmic objects are shown at the start with their according mass, ranging from lowest (Asteroid) to largest (Andromeda).",

    "Exoplanet Game": "Make a judgement if a planet is habitable or not. If yes, one can deploy a probe; if not, one can skip it. Find sufficient number of habitable exoplanets to succeed the mission.",

    "Galactic Golf": "This \"game\" is 100% hand coded. AI was only used twice to guide a fix. The goal of the game is to get the spaceship (blue ball) to the core (white dot at centre of screen), while avoiding Lebron. The background is provided by a user-supplied .fits file (feel free to use your own), where the intensities dictate the slowdown of the spaceship. Use the left and right arrow keys to change the direction before shooting. Use the up and down arrow keys to choose the shot power. Press the spacebar to shoot. Try to find all 3 secret achievements.",

    "Galactic Shooter": "A bullet hell shooter where the player, as Freddy Fazbear IN SPACE, can move around and shoot the enemy m101.fits with beloved ProgNum student Joe, moving throughout a beautiful fits file skyline! Try to score as high as you can by shooting the m101.fits enemies and survive as long as possible!\n\n"
        "Controls:\n    "
            "WASD - Move (W - up, A - left, S - down, D - right)\n    "
            "Space - Shoot the Joe projectiles.\n"
        "At the game over screen:\n    "
        "Esc - Exit the game\n    "
        "R - Restart; start a new round of the game",

    "Galaxy Finder": "Space Invaders variation 'Galaxy Finder'. You shoot a beam and catalogue each galaxy. Game ends when all galaxies in the Local Group are added or a galaxy escapes the range of the beam (goes off-limits).",

    "Galaxy Matcher": "Click and flip galaxy images to find the matched ones.",

    "Gambling Game": "In this game, one must gamble to achieve the correct ending. Thou must not loose all your money. Beware!!!!! This is some sketchy territory! You might need to close some pesky astronomy files!",

    "GeoGuesser": "Basically geoguesser but with galaxies (unfortunetely only 2). An image will appear in front of you , and your task is to guess what the Galaxy name is from the available options. You might get a fun fact as a reward\n\n"
        "[yellow]IMPORTANT NOTE: Unfortunately, certain documents required to run this game was not provided by the creator, so the game is currently unplayable.[/yellow]",

    "HorizonScape": "HorizonScape is an interactive escape game playable on any terminal that can run a python executable script. The user is the captain of a spaceship and has to control it by providing the correct inputs.\n\n"
        "How to play:\n    "
        "The main part of the game is analogous to the popular game ‘Hangman’, where one player thinks of a word and the other guesses it by guessing one letter at a time. In that game, if the guess of player2 is right, player1 shows which letter of the word it is, if not, player1 makes a drawing of a man being hung one line at a time. In HorizonScape, the word is embedded in the code, player1 is therefore the computer, while player2 is the user, who has to guess it one letter at a time. In the case of a correct guess, the position of the letter is shown, otherwise a picture is being shown that decreases in size with each wrong guess.\n    "
        "The user can play this game by running the executable script on a terminal. It is recommended that after the system outputs plots, the user clicks back onto the window of the terminal to continue playing, therefore, full size terminal window is not recommended, in order to be able to see the pictures. The game provides instructions on what the next step is, so just sit back and enjoy!",

    "Intergalactic Travel": "The game lets you explore the universe by conducting a cone search for a chosen set of parameters. It provides some information on a celestial object from the chosen patch of sky, including a native species of not so chill aliens living there. The not so chill aliens ask you 5 trivia questions, if you answer at least 3 correctly then Earth stays protected! Otherwise...",

    "Ionise HI Clouds": "Choose the photon frequency (energy). By clicking the left mouse, you will shoot photons. The goal is to ionise all the electrons in the window.", 

    "Management Sim": "You are a science project manager, leading expedition amongst different star systems. During the expedition, you can choose to <Survey> the systems, <Mine> useful resources, <Upgrade> anything related to your project, <Scan> the systems, or <Pass>, in this round. When running out funds, morales, or expiry, the game ends.",

    "Medicine across the Universe": "You are on Pluto and need to go to Mercury. Take your ship and you have to make decisions on what do to. Moving to another planet will take you electricity. Everyday you need to eat. You can produce food but it needs electricity. Be careful, if you run out of electricity, you cannot move anymore and are stuck in space forever but if you run out of food, you will die. And the clock is ticking, so don't take too much your time. \n\n"
        "HOW TO PLAY: \n    ""It is very intuitive : just answer the questions and make decision based on what is happening. \n\n"
        "IMPORTANT: \n    ""For the game to be running please input the available options only, otherwise you will just skip to the next day.",

    "Memorising Galaxies": "You have departed Earth and are in a space ship (your call name is Anaconda 7) on a journey. You receive a mission from Earth to find the coordinates of a galaxy, so you can travel to it. By matching two galaxies together, you can obtain the correct coordinates. At the end, you have to enter the coordinates you found. If the coordinates are correct, you can continue your space life as normal, waiting on the next mission. If the coordinates are wrong, you have to restart the game! So be very careful when typing and pay close attention to the mission description!",

    "New Home": "The user chooses a new galaxy and star for humanity, and then creates a planet. If the user is not careful, the planet will not be habitable.",
    "Planet Explorer": "In this game you are going on a journey across the stars. You are a discovering astronaut and you are going to fly to a planet and make discoveries about the planet. You are given choices upon landing, choices which will have consequences, some may be good, some may be bad. At a first playthrough you might not get a positive outcome, but worry not, you can always play again!",

    "Puzzle Game": "Try to put the pieces in the right place!",

    "Save the Ship": "In this text-based adventure game, you are in your spacecraft, when the alarms suddenly go off. When you wake up you find out that the ship's systems are failing causing it to become destabilized. The only way you can survive is by restoring the spacecraft yourself. Navigate your way through the ship and solve puzzles to ensure it doesn't go down!",
    "Solar System Memory Game": "In this game, you can play Memory with the dwarf(planets) of our own Solar System. With an extra easter egg :), one of the planets is not there, can you find it and be the master of our Solar System?",

    "Sombrero": "This game tests your astronomical tastes, with a series of galaxies with werid names! You get to answer questions about some silly galaxies, and also learn a lot about sombreros (not always the galaxy). There is a more 'serious' ending, where you get to see the peak wavelengths of the sombrero galaxy from real data!\n\n"
    "INSTRUCTIONS:\n    "
    "- you have to put a text/number response to prompts\n    "
    "- After each image is created, you have to close the window to continue; remember it well!",

    "Space Invaders": "Space Invaders. Press <space> to shoot the alien ships.",

    "Space Rescue Game": "Space Rescue is a text-based game where you travel between planets to rescue stranded astronauts. Each trip costs fuel based on distance, and planetary conditions can damage your ship. You collect points and may encounter random events that help or harm you. The goal is to rescue enough astronauts within a limited number of turns while managing your fuel and health.", 

    "Spaceworm": "In the dark, vast regions of space...\n\n"
        "You are a very hungry spaceworm, traveling through mostly empty space. Occasionally though, you stumble on beautiful bright stars, ripe with thermonuclear fusion and ready for you to eat!\n\n"
        "In spirit of the retro Snake game, use the arrow keys to move around a square region of space and eat the stars! Be careful - you cannot hit the edges of the screen or yourself. If you do die, the game gives you some fun information about the star you failed to consume before your death.\n\n"
        "Try to grow as much as you can, learn some facts about stars you can see in the night sky, and most importantly, have fun!",

    "Star Explorer": "The goal of this game is to guess the correct star, based on the hints given. If you guess wrong the first time, you get more hints. You have 5 lives total.",

    "Star Wars": "In this game you name and design your own star! Then, you go against other stars. The battle is based on your stars properties. The more superior star will win!\n\n"
        "Instructions:\n    "
        "1. Name your star.\n    "
        "2. You have a limited amount of coins to use. Choose mass, luminosity and velocity.\n    "
        "3. The game gives you a random star to fight against.\n    "
        "4. Choose an approach: Aggressive, Evasive or Balanced. In aggressive, the mass of the stars matters most. In evasive, your velocity matters most. In balanced, all properties matter.\n    "
        "5. Your success depends on your stars properties against the other stars properties. If you win, you can choose to continue paying. If you lose, game is over and you can restart.",

    "Stellar Evolution Simulator": "Take a journey along an HR diagram by helping a star achieve its dream! The player gets to pick between a sun-like star and a massive star, which give two different game paths. The player will receive a trivia question at each step of the stellar evolution ladder, and have two attempts at answering it in order to progress.\n\n"
        "In order to play the game, the player must input the correct answer to astronomy trivia questions (related to the stage of stellar evolution that the star is at). In order to play it correctly on terminal, the player needs to close the plotted HR diagrams before moving onto the next part of the game. the player should also put a space before each of its answers, due to the way terminal processes the input.\n\n"
        "Enjoy the game!",

    "Sunglasses in Space": "The goal is to acquire as much data from stars as possible. The player controls a spaceship and flies through a 2D star field created from the 'ra', 'dec' coordinates and 'phot_g_mean_mag' data from Gaia. The player needs to first acquire their sunglasses and then fly to target stars meanwhile dodging or shooting at randomly spawn enemy spaceships that chase the player.\n\n"
    "How to play:\n    "
        "- Press 'W' 'A' 'S' 'D' for movement (up, left, down, right)\n    "
        "- Press 'SPACE' to shoot bullets. You shoot left or right, based on your last movement direction. Shooting an enemy kills them immediately.\n    "
        "- First you need to fly to the drawn sunglasses on screen to acquire your sunglasses.\n    "
        "- Press 'E' to put your sunglasses off/on (possible after acquiring the sunglasses)\n\n"
    "Sunglasses mechanics:\n    "
        "- With sunglasses put on: You cannot shoot bullets. The stars are dimmed and you see a blue target star where you need to go to acquire data. The next target star turns blue when you've reached the previous blue target star.\n    "
        "- With sunglasses put off: You can shoot bullets. The stars are brighter and if you get too close to a star the screen goes grey because you are temporarily blinded.\n\n"
    "Gameover:\n    "
        "- When hit by an enemy spaceship, the game ends\n    "
        "- You see your score: data acquired from the amount of stars",

    "Sweet Saviour": "Welcome to SWEET SAVIOUR! \n\n " 
        "A story based astronomy game in which you are tasked to save the world. \n\n"
        "INSTRUCTIONS: During the story's progression you will be presented with questions and dilemma's. Answer correctly or there might be consequences. In total there are 3 differend endings, try to get them all!",
        
    "The Planet Defender": "The goal is simple -- it is to defend the Moon, Mars and the Earth which are under attack by many waves of meteors. You are given a ship that can shoot bullets to take down the asteroids. You can move the ship around the planet using the arrows and shoot using the space bar. As the levels progress, so does the gravity of the protected bodies which cause the meteors to fall faster and faster. So in the end, the game can become quite challenging. Astronomical calculations were used to simulate the gravity of the falling meteors however were adjusted by a factor to speed them up otherwise they would appear too slow in game, for the pixel window of the game. The waves of meteors also increase as you progress adding a further difficulty to the game.",

    "Tim Shooter Game": "Use you arrows to move around m101 and make sure not to get hit by Tim, the scary TA. You can shoot him by using the space bar!",

    "Travel to Exoplanet": "In this game, you have to find a password to travel to an exoplanet in a distant galaxy and find a new home for humanity.\n\n"
        "[yellow]IMPORTANT NOTE: Unfortunately, the main image required to run this game was not provided by the creator, so the game is currently unplayable.[/yellow]",

    "Virtual Telescope Project": "Have you ever dreamt of owning a seestar telescope? (Just to clarify, I haven't.) Then you will definitely enjoy the Virtual Telescope Project VTP! With VTP you can control a virtual telescope located in Groningen, look for interesting targets around the sky (if they are visible, of course) and observe them using ESA Skyview.\n\n"
        "IMPORTANT!\n    "
            "So far the input variables (Right Ascension,Declination, Field of View) are only accepted in degree units. The telescope might start making very strange movement while changinig target. Do not worry, the result will be the one given, debugging is still in progress.\n\n"
        "HOW TO PLAY\n    "
            "There are three Entries where you can enter celestial coordinates to point the telescope onto. Then by pressing Go to target you can change the telescope's position. You also can start an observation by pressing Start observation. Also, you can turn on and off the telescope's ability to keep track of the position it is in by pressing Tracking ON/OFF.\n\n"
        "RECENT BUG FIXES\n    "
            "Telescope cannot observe below the horizon. Right Ascension calculation result in the right value",

    "Voyage": "This is a storyline driven game where you are an astronaut going on a voyage in the universe. You have finally reached your most beautiful destination, but then suddenly your spaceship is hit by something. Your spaceship slowly starts breaking down, but there is a way for you to save yourself and your spaceship.\n\n"
        "By guessing the correct astronomy themed word (hangman), you will save the spaceship. But if you do not guess the word in 9 tries, there sadly is nothing else left to be done. It is game over for you.\n\n"
        "Come play this fun and exciting storyline driven game now!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
}

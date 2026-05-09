"""
Astronomy Constellation Quiz Game
--------------------------------
This game shows constellation images and asks the user to type their names.

Rules:
- 20 random questions from 31 constellations
- Case-sensitive answers
- 3 attempts per question
- "SKIP" skips the question
- Timer limits total game time

Dataset:
All astronomical images are taken from kaggle:
https://www.kaggle.com/datasets/theprakharsrivastava/stargazer
"""

# Importing required libraries
import random                                       # For selecting random images
import time                                         # For timer functionality
import os                                           # For handling file paths
from tkinter import Tk, Canvas, Label, PhotoImage   # For displaying images in a window


class ConstellationGame:
    """
    Main class that will control the entire game.
    Uses Object-Oriented Programming (OOP).
    """

    def __init__(self):
        """
        Initializator method.
        Runs automatically when a new game object is created.
        Initializes all variables.
        """

        # Folder where constellation images are stored
        self.image_folder = "images/"

        # Folder where alien images are stored
        self.alien_folder = "alien_cat/"

        # Dictionary mapping image file names to correct answers
        # Key = image filename
        # Value = correct constellation name (case-sensitive)
        self.constellations = {
            "andromeda.png": "Andromeda",
            "aquila.png": "Aquila",
            "aries.png": "Aries",
            "bootes.png": "Bootes",
            "cancer.png": "Cancer",
            "canis_major.png": "Canis Major",
            "capricornus.png": "Capricornus",
            "cassiopeia.png": "Cassiopeia",
            "cepheus.png": "Cepheus",
            "columba.png": "Columba",
            "crux.png": "Crux",
            "cygnus.png": "Cygnus",
            "draco.png": "Draco",
            "gemini.png": "Gemini",
            "hercules.png": "Hercules",
            "hydra.png": "Hydra",
            "lacerta.png": "Lacerta",
            "leo.png": "Leo",
            "lepus.png": "Lepus",
            "libra.png": "Libra",
            "lyra.png": "Lyra",
            "orion.png": "Orion",
            "pavo.png": "Pavo",
            "perseus.png": "Perseus",
            "pisces.png": "Pisces",
            "sagittarius.png": "Sagittarius",
            "scorpius.png": "Scorpius",
            "taurus.png": "Taurus",
            "ursa_major.png": "Ursa Major",
            "ursa_minor.png": "Ursa Minor",
            "virgo.png": "Virgo"
        }

        # Player score starts at 0
        self.score = 0

        # Will store the 20 randomly selected questions
        self.selected_questions = []

        # Stores all answers shown at the end
        self.answers_log = []

        # Time limit for the game (in seconds)
        self.time_limit = 300

    def show_image(self, image_path):
        """
        Displays an image in a Tkinter window.
        Uses subsample() to resize the images.
        Parameters: image_path (str) - path to the image file
        Returns: root (Tk object) - window so we can close it later
        """

        # Creating a new window and giving it a title
        root = Tk()
        root.title("Constellation")
        
        # Loading the image file and resizing it
        img = PhotoImage(file=image_path)
        img = img.subsample(2,2)  # half size
        
        # Creating a label widget to hold the image
        label = Label(root, image=img)
        
        # Putting the label into the window
        label.pack(expand=True) # helps with centering
        label.image = img
        root.img = img
        
        # Updating window so it actually shows
        root.update()

        # Returnign the window object (so we can close it later)
        return root

    def start_screen(self):
        """
        Shows the starting alien image and waits for user input.
        """

        # Creating full path to start image and showing the image
        path = os.path.join(self.alien_folder, "start.png")
        root = self.show_image(path)

        # Waiting for user to press Enter to start the game
        input("Press ENTER to start the game...")

        # Closing the window
        root.destroy()

    def show_rules(self):
        """
        Displays the game rules before starting.
        """

        print("\n======= GAME RULES =======")
        print("- Type the constellation name in Latin (no need for special characters)")
        print("- Case sensitive (capitalize first letter of each word, where necessary!)")
        print("- You have 3 attempts per question, then the question gets skipped")
        print("- Type 'SKIP' to skip a question")
        print("- Skipped questions = 0 points")
        print("- Correct answer = 1 point")
        print("- You must press ENTER after each guess")
        print(f"- Time limit: {self.time_limit // 60} minutes")
        print("=============================\n")

        input("Press ENTER to continue...")

    def end_screen(self):
        """
        Shows an ending image depending on player's score.
        """

        # If perfect score, then win image
        if self.score == 20:
            img = "win.png"

        # If very low score, then lose image
        elif self.score < 7:
            img = "lose.png"

        # Otherwise no image
        else:
            img = None

        # Only show image if one is selected
        if img:
            path = os.path.join(self.alien_folder, img)

            root = self.show_image(path)

            input("Press ENTER to continue...")

            root.destroy()


    def confetti(self):
        """
        Displays animated star confetti using Tkinter if player gets 20/20.
        """

        # Creating window
        root = Tk()
        root.title("Celebration!")

        # Creating canvas
        canvas = Canvas(root, width=600, height=400, bg="black")
        canvas.pack()

        # List for the stars confetti
        stars = []

        # Creating random stars
        for _ in range(100):
            x = random.randint(0, 550)
            y = random.randint(0, 350)
            size = random.randint(15, 40)

            # Making the stars
            star = canvas.create_text(x, y, text="*", font=("Arial", size), fill="yellow")
            stars.append(star)

    # Animation function
        def animate():
            for star in stars:
                canvas.move(star, 0, random.randint(10, 30))  # moving down so it looks like falling

                # Reseting if off screen
                coords = canvas.coords(star)
                if coords[1] > 400:
                    canvas.move(star, 0, -400)

            root.after(50, animate)  # repeating animation

        animate()
        root.update()

        # Closing window after 4 seconds
        root.after(4000, root.destroy)
        root.mainloop()


    def play(self):
        """
        Main game loop:
        - Starts game
        - Loops through questions
        - Handles input and scoring
        """

        # Showing starting screen and rules
        self.start_screen()
        self.show_rules()

        # Randomly pick 20 constellations from dictionary
        self.selected_questions = random.sample(list(self.constellations.items()), 20)

        # Record start time
        start_time = time.time()

        # Loop through selected questions
        for idx, (filename, answer) in enumerate(self.selected_questions):

            # Checking if time limit exceeded
            if time.time() - start_time > self.time_limit:
                print("\nTime is up!")
                break

            # Showing question number
            print(f"\nQuestion {idx + 1}/20")

            # Building image path and showing the constellation image
            path = os.path.join(self.image_folder, filename)
            root = self.show_image(path)

            # Attempts counter
            attempts = 0

            # Flag to check if answered correctly
            correct = False

            # Allowing up to 3 attempts
            while attempts < 3:

                # Getting user input
                guess = input("Your answer: ")

                # If user types SKIP, then skip question
                if guess == "SKIP":
                    print("Skipped!")
                    break

                # If correct answer, then it adds a point to the score
                if guess == answer:
                    print("Correct!")

                    # Increasing the score
                    self.score += 1

                    correct = True
                    break

                else:
                    # Wrong answer increases attempts
                    attempts += 1

                    print(f"Wrong! Attempts left: {3 - attempts}")

            # If user failed all attempts shows correct answer
            if not correct and attempts >= 3:
                print(f"Answer was: {answer}")

            # Saving result for final review at the end
            self.answers_log.append((idx, answer))

            # Closing image window
            root.destroy()

        # After all questions are answered, it shows results
        self.show_results()

        # Showing ending image
        self.end_screen()


    def show_results(self):
        """
        Displays final score and all correct answers.
        """

        print("\n======= GAME OVER =======")

        # Printing final score
        print(f"Final Score: {self.score}/20")

        # If perfect score, then show confetti
        if self.score == 20:
            self.confetti()

        # Final message
        print("\nPlay again! At 20/20 you will make Gleep Glorp proud!")


# Entry point of the program
if __name__ == "__main__":

    # Creating a game object
    game = ConstellationGame()

    # Starting the game
    game.play()
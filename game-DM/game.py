#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random

class Player:
    """Represents the player and keeps track of lives and progress."""

    def __init__(self, name: str, lives: int = 3):
        """Create a new player with a name and starting lives."""
        self.name = name
        self.lives = lives
        self.position = 0
        self.correct_answers = 0

    def lose_live(self):                                     # Only returns an action
        """Reduce player lives by one live."""
        self.lives -= 1

    def move_forward(self):                                  # Only returns an action
        """Move the player one step closer to escape."""
        self.position += 1
        self.correct_answers += 1

    def is_alive(self):                                      # Returns True or False
        """Return True if the player still has lives."""
        return self.lives > 0


class Question:
    """Stores a multiple-choice astronomy question."""

    def __init__(self, prompt: str, options: list[str], answer: str, fact: str):
        """Initialize the question, answer options, correct answer, and a fun fact."""
        self.prompt = prompt
        self.options = options
        self.answer = answer.upper()       # To make sure the answer is a capital letter
        self.fact = fact

    def ask(self):                         # Returns True or False
        """Display the question, collect an answer, and return True if correct."""
        print("\n" + "=" * 60)             # For lay-out purpuse
        print(self.prompt)                 # Prints the question
        for option in self.options:        # Prints the answer options under eachother
            print(option)

        # To make sure the answer input is A, B, C or D:
        user_answer = input("Your answer (A/B/C/D): ").strip().upper()
        while user_answer not in ["A", "B", "C", "D"]:
            user_answer = input("Please enter A, B, C, or D: ").strip().upper()

        if user_answer == self.answer:
            print("✅ Correct! You can enter the next room!")
            print(f"Did you know? {self.fact}")
            return True

        else:
            print("❌ Wrong! The aliens got closer...")
            print(f"The correct answer is {self.answer}.")
            print(f"Did you know? {self.fact}")
            return False


class AlienEscapeGame:
    """Main game class for the alien escape quiz."""

    def __init__(self):
        """Create the game state and load astronomy questions."""
        self.player = None                                # No player created yet
        self.questions = self.load_questions()            # Calls the function load_questions
        random.shuffle(self.questions)                    # Randomly shuffles the questions
        self.escape_distance = 5                          # Needs 5 correct answers to escape

    def load_questions(self):                             # Returns a list of Question objects from the class Question
        """Load astronomy questions based on real Solar System data."""

# Data is used from https://science.nasa.gov/solar-system/planets/
        
        return [
            Question(
                "Which planet is the largest in our Solar System?",
                ["A. Earth", "B. Jupiter", "C. Mars", "D. Venus"],
                "B",
                "Jupiter is so large that 1,000 Earths could fit inside it."
            ),
            Question(
                "Which planet is closest to the Sun?",
                ["A. Mercury", "B. Venus", "C. Earth", "D. Mars"],
                "A",
                "Mercury has extreme temperatures ranging from -180°C to 430°C."
            ),
            Question(
                "Which planet is famous for its prominent ring system?",
                ["A. Neptune", "B. Uranus", "C. Saturn", "D. Mars"],
                "C",
                "Saturn’s rings are made of billions of ice particles, some as small as dust and others as large as mountains."
            ),
            Question(
                "Which planet is known as the Red Planet?",
                ["A. Jupiter", "B. Mercury", "C. Mars", "D. Venus"],
                "C",
                "Mars was named by the ancient Romans for their god of war because its reddish color was reminiscent of blood."
            ),
            Question(
                "Which planet has the most known moons?",
                ["A. Earth", "B. Jupiter", "C. Venus", "D. Mercury"],
                "B",
                "Some of Jupiter’s moons, like Europa, may have oceans beneath their icy surface."
            ),
            Question(
                "Which planet is hottest on average, even hotter than Mercury?",
                ["A. Venus", "B. Jupiter", "C. Mars", "D. Saturn"],
                "A",
                "Venus is the hottest planet because of its extreme greenhouse atmosphere."
            ),
            Question(
                "What is the name of our galaxy?",
                ["A. Andromeda", "B. Whirlpool", "C. Milky Way", "D. Sombrero"],
                "C",
                "The Milky Way contains over 100 billion stars."
            )
        ]

    def intro(self):                   # Only returns an action (the introduction)
        """Display the game introduction and create the player."""
        print("👽 WELCOME TO ALIEN ESCAPE 👽")
        print("You are trapped on a spaceship by aliens.")
        print("To unlock each door, answer astronomy questions correctly.")
        print("Each correct answer moves you closer to your escape shuttle.")
        print("Each wrong answer costs 1 live. You start with 3 lives.\n")
        name = input("Enter your astronaut name: ").strip()       # Name of the player
        if not name:
            name = "Mysterious"
        self.player = Player(name)     # New player object with name stored in self.player

    def show_status(self):
        """Print the player's current lives and escape progress."""
        print("\n" + "-" * 60)
        print(f"Astronaut: {self.player.name}")
        print(f"lives: {self.player.lives}")
        print(f"Escape progress: {self.player.position}/{self.escape_distance}")
        print("-" * 60)

    def play_turn(self, question: Question):
        """Play one turn using a single question."""
        self.show_status()
        if question.ask():                   # If it gives True (so correct answer)
            self.player.move_forward()
        else:
            self.player.lose_live()

    def has_won(self):                       # Returns True or False
        """Return True if the player reached the escape shuttle."""
        return self.player.position >= self.escape_distance

    def ending(self):
        """Display the final result of the game."""
        if self.has_won():
            print("\n🚀 You escaped the alien spaceship and returned to Earth!")
            print(f"Final score: {self.player.correct_answers} correct answers.")
        else:
            print("\n👽🛸 The aliens captured you before you reached the shuttle...")
            print(f"Final score: {self.player.correct_answers} correct answers.")

    def run(self):
        """Run the full game loop until the player wins or loses."""
        self.intro()

        for question in self.questions:
            if not self.player.is_alive() or self.has_won():
                break
            self.play_turn(question)

        self.ending()

game = AlienEscapeGame()  # To run the game
game.run()


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random


class GalaxyGame:
    """
    Astronomy game:
    In this game, you get a small cut out part of a bigger image of a galaxy. Through this image, you have to find where 
    you are in the bigger image. If you think you know where you are, you can click on that point in the bigger image. The closer
    you are to the actual random point, the more points you obtain
    """

    def __init__(self, image_path):
        """Loading the png image and initializes the game."""
        self.image = np.array(Image.open(image_path))
        self.height, self.width, _ = self.image.shape
        self.score = 0  # Setting score

    def get_random_patch(self, size=200):
        """Finds a random small piece of the total image"""
        x = random.randint(0, self.width - size)
        y = random.randint(0, self.height - size)

        patch = self.image[y:y+size, x:x+size]

        center_x = x + size // 2
        center_y = y + size // 2
        return patch, center_x, center_y

    def play_round(self):
        """This function runs the rounds of the game. The code in here, together with the onclick definition
           make it possible for the game to show both images and let the player click somewhere in the image.
        """
        patch, true_x, true_y = self.get_random_patch()  # Using self defined function to find a random patch of the image.
        self.guess = None

        fig, axes = plt.subplots(1, 2, figsize=(20, 10))

        # Shows the zoomed in part of the picture
        axes[0].imshow(patch)
        axes[0].set_title("Zoomed-in galaxy region")
        axes[0].axis("off")

        # Shows the full picture, in which you eventually click
        axes[1].imshow(self.image)
        axes[1].set_title("Click where this region comes from")

        def onclick(event):
            """Takes in the user's click."""
            if event.inaxes == axes[1]:
                self.guess = (int(event.xdata), int(event.ydata))
                plt.close()

        fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show()

        if self.guess is None:  # If no click is found, it returns this message
            print("No click detected!")
            return

        guess_x, guess_y = self.guess

        self.calculate_score(guess_x, guess_y, true_x, true_y)  # Calculating the score
        self.show_result(true_x, true_y, guess_x, guess_y)  # Displaying the result

    def calculate_score(self, guess_x, guess_y, true_x, true_y):
        """
        The score is calculated based on the distance from the actual point.
        """

        distance = np.sqrt((guess_x - true_x)**2 + (guess_y - true_y)**2) # Calculating distance

        points = int(100 * np.exp(-distance / 80))  # calculating amount of points based on distance

        self.score += points

        print(f"\nDistance: {distance:.2f}")
        print(f"Points this round: {points}")
        print(f"Total score: {self.score}")

    def show_result(self, true_x, true_y, guess_x, guess_y):
        """This function shows what the actual patch was and which point the user guesses"""

        plt.imshow(self.image)

        # Correct location (top-left of patch)
        plt.scatter(true_x, true_y, color='green', label='Correct location')

        # User guess
        plt.scatter(guess_x, guess_y, color='red', label='Your guess')

        # Show actual patch area
        rect = plt.Rectangle(
            (true_x, true_y),
            200, 200,
            linewidth=2,
            edgecolor='green',
            facecolor='none'
        )
        plt.gca().add_patch(rect)

        plt.legend()
        plt.title("Result")
        plt.show()

    def play(self, rounds=1):
        """Main game loop."""

        for i in range(rounds):
            print(f"\n--- Round {i+1} ---")
            self.play_round()

        print(f"\n FINAL SCORE: {self.score}")


if __name__ == "__main__":
    game = GalaxyGame("stsci-01g8jzq6gwxhex15pyy60wdrsk-2.png")
    game.play(1)


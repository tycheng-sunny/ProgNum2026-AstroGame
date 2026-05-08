#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk  # To have a graphical interface that can handle the cards and interactions.
import os
from astropy.io import fits
import numpy as np
from matplotlib.pyplot import figure, show
import matplotlib.pyplot as plt  #  Necessary to close the figure.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # To convert figures to a format Tkinter can display.
from PIL import Image, ImageTk  # To convert and display image to/in Tkinter.
import random
from tkinter import messagebox  # To displat message after entry.

def Introduction(text):
    """A function that opens and prints the introduction when called"""
    with open(text, 'r') as file:  # The with statement ensures the file is closed again after reading
        script = file.read()
    return print(script)  # Print the contents.

class GalaxyObject:
    """ A class to define the galaxies used.

    Attributes:
        filename (str): The input filename of a galaxy.

    Methods:
        plot_galaxy(self): Plots the galaxy to use as an image.
        match_found_fact(self): Prints a fact about a matching set of cards.
    """
    def __init__(self, filename):
        """Initializes the galaxy object by locating the FITS file."""
        base_path = os.path.dirname('Images/')  # Create a path to the directory where the images are.
        full_path = os.path.join(base_path, filename)  # Join with filename to make uniform path.
        self.file_path = full_path  # Initialize the full path.
        self.hdulist = fits.open(self.file_path)  # Get the HDU list from the file.
    
    def plot_galaxy(self):
        """ A function that plots the galaxy in the FITS file
                
            Parameters: any of the initialized values.
            Return: a figure of the data obtained through the initialization.
        """
        data = self.hdulist[0].data  # Get image data.
        
        fig = figure(figsize=(8, 8)) # Create a figure.
        frame = fig.add_subplot(1,1,1)
        frame.imshow(data)  # Show data.
        frame.set_axis_off()  # Remove the axes and ticks.
        return fig
    
    def match_found_fact(self): 
        """ A function that gives the RA and DEC of the matched galaxy.
            
            Parameters: any of the initialized values.
            Return: a statement containing the coordinates, retrieved from the header, about the matched galaxy pair.
        """ 
        hdr = self.hdulist[0].header  # Get header.
        RA = hdr['OBJCTRA']
        DEC = hdr['OBJCTDEC']
        statement = f"The galaxy is located at RA = {RA} h min s and DEC = {DEC} deg arcmin arcsec"
        return statement

class Card:
    """ A class to create a card for each galaxy.
    
    Attributes:
        root : Name for the Tkinter window.
        filename (str): The input filename of a galaxy.

    Methods:
        create_image(self): Makes a Tkinter image, through pillow, of the plot made in GalaxyObject by calling the plot_galaxy() function.
    """
    def __init__(self, root, filename):
        self.root = root  # Save 'root' window into permanent memory, so other functions can 'çommunicate' with the main window.
        self.galaxy = GalaxyObject(filename)  # Initialize the plot so it can be used inside this class.
        self.is_visible = False  # Variable to store if card is visible.
        self.filename = filename

    def create_image(self):
        """ A function that creates the galaxy image in Tkinter format.
            
            Parameters: any of the initialized values.
            Return: an image of the plotted galaxy.
        """
        #if self.galaxy_image is None:  # Creates image only if it doesn't exist yet.
        figure = self.galaxy.plot_galaxy()  # Store the plotted galaxy as a figure.
        canvas = FigureCanvasTkAgg(figure, master=self.root)  # Translate from Matplotlib to Tkinter and put plot in the window (root).
        canvas.draw()  # Similar to plt.show(): makes sure canvas is actually shown/drawn.

        rgba_buffer = canvas.buffer_rgba()  # Get the buffer.
        
        # Translate to RGBA buffer (gives Pillow a view of the plot), then to Tkinter image.
        img = Image.frombuffer('RGBA', canvas.get_width_height(), rgba_buffer, 'raw', 'RGBA', 0, 1)  # Get image through buffer.
        img = img.convert('RGB').resize((200,200))  # Convert to RGB to remove transparency and resize to not fill entire screen.
        image = ImageTk.PhotoImage(img)  # Display as image.
        
        plt.close(figure)  # Removes figure from Matplotlib memory to not overload it.
        return image

class Game:
    """ A class that holds the main game mechanism.
    
    Attributes:
        root : Name for the Tkinter window.
    
    Methods:
        create_widgets(self): Creates the widgets (user interactive additions to the window), in this case a grid with 16 buttons.
        on_card_click(self, card, index): Creates the image on the button when its clicked on. Refers to the match function if two cards are clicked.
        check_match(self): Checks if two cards are a match.
        match_found(self, card_1, card_2, index_1, index_2): Locks the two buttons of the match and prints a fact abput the galaxy using match_fount_fact.
        turn_back(self, index_1, index_2): Turns back cards when the images do not match.
        quit_game(self): Makes a button that quits the game when clicked.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Collect the Galaxies")  # Set title of the window.
        self.root.geometry('{}x{}'.format(800, 600))  # Define shape of window.
        
        self.files = ["m101.fits", "m101.fits", "bode.fits", "bode.fits", "black_eye.fits", "black_eye.fits", 
                      "fireworks.fits", "fireworks.fits", "cigar.fits", "cigar.fits", "m32_2.fits", "m32_2.fits",
                      "antennae.fits", "antennae.fits", "cent_A.fits", "cent_A.fits"] # Doubled files for a pair
        random.shuffle(self.files)  # Shuffle/reorder the list.
        self.cards = [Card(self.root, file) for file in self.files]  # Create a card for each file (pairs).
        self.buttons = []  # A list for the card buttons so the program remembers them.
        self.buttons_frame = []  # A list for the other buttons so the program remembers them.
        self.flipped_cards = []  # A list for the flipped cards to check if cards are flipped.
        self.matches = []  # A list for the matched pairs.
        self.is_processing = False  # Prevent clicking while turning back cards (makes sure system does not crash).
        
        # Define the frames (like a rectengular/square patch in the window)
        self.title_frame = tk.Frame(self.root, bg='navy', width=400, height=50)
        self.card_frame = tk.Frame(self.root, bg='white', width=400, height=200)
        self.entry_frame = tk.Frame(self.root, bg='white', width=400, height=50) 
        self.quit_frame = tk.Frame(self.root, bg='gray2', width=400, height=50)

        # Layout: we have rows and columns (only rows in this case)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.title_frame.grid(row=0, column=0, sticky="ew")
        self.card_frame.grid(row=1, column=0, sticky="nsew")
        self.card_frame.grid_propagate(False)  # Refrains frame from shrinking
        self.entry_frame.grid(row=2, column=0, sticky="ew")
        self.quit_frame.grid(row=3, column=0, sticky="ew")

        title_label = tk.Label(self.title_frame, text='COLLECT THE GALAXIES', fg='white', bg='navy', font=('Courier', 20, 'bold'))
        title_label.grid(row=0, column=0, pady=10)  # Add title in window.
        self.title_frame.grid_columnconfigure(0, weight=1) # Center the title

        # Create the buttons by calling the functions that contain a tk.Button or tk.Entry command.
        self.create_widgets()
        self.quit_game() 
        self.coordinate_entry()
        
    def create_widgets(self):
        """ A function that creates the interactive widgets (the 4x4 button grid).
            
            Parameters: any of the initialized values.
            Return: a 4x4 grid of buttons that show an image if clicked on.
        """
        # Create frame (4x4) inside card_frame.
        for x in range(4):
            self.card_frame.grid_columnconfigure(x, weight=1, uniform="group1")  # Make column for x. Uniform states that all buttons must stay the same size.
            self.card_frame.grid_rowconfigure(x, weight=1, uniform="group1")  # Make row for x. Weight decides how the space (of a frame or in a frame) is divided.
        
        for i, card in enumerate(self.cards):  # Enumerate over the list containing the cards.
            button = tk.Button(self.card_frame, text="?", width=20, height=20, command=lambda c=card, i=i: self.on_card_click(c, i))  # Parent window, then parameters. Create function to represent current card.
            button.grid(row=i//4, column=i%4, sticky="nsew", padx=1, pady=1)  # Create grid based on index number
            self.buttons.append(button)   # Append button to remember in game (so it doesn't disappear).
    
    def on_card_click(self, card, index):
        """ A function that displays an image if it was clicked on.
            
            Parameters: any of the initialized values, the card value and its index.
            Return: none.
        """
        if not self.is_processing or card.is_visible:  # Only show image on a clicked button if the system is not still processing or is visible = true.
            # If the button was clicked on, create an image on it. 
            card_image = card.create_image()  # Generate image for clicked card.
            self.buttons[index].configure(image=card_image)  # Update button display to image.
            self.buttons[index].image = card_image  # Link image to button with specific index.
            card.is_visible = True
    
            self.flipped_cards.append((card,index))  # Add the card and its index to the list.
            
        if len(self.flipped_cards) == 2:
            self.is_processing = True  # Lock clicks: you cannot click another card.
            self.check_match()  # Check for match.

    def check_match(self):
        """ A function that checks for a match between two cards.
            
            Parameters: any of the initialized values.
            Return: none.
        """
        card_1, index_1 = self.flipped_cards[0]  # Get data first card.
        card_2, index_2 = self.flipped_cards[1]  # Get data second card.

        if card_1.filename == card_2.filename:  # Check if names match.
            self.root.after(1000, lambda: self.match_found(card_1, card_2, index_1, index_2))  # After one second, call the function match_found. Without lambda: immediatly goes to match_found. 
        else:
            self.root.after(1000, lambda: self.turn_back(index_1, index_2))  # After one second, call the function turn_back. Without lambda: immediatly goes to turn_back, user doesn't even see second card.
    
    def match_found(self, card_1, card_2, index_1, index_2):
        """ A function that disables the cards after they match and prints a fact about the matched galaxy.
            
            Parameters: any of the initialized values, card_1, card_2, index_1 and index_2 (The values and indices of the two cards).
            Return: none.
        """
        print("You found a match!")
        print(GalaxyObject(card_1.filename).match_found_fact(), "\n")

        # Update buttons to no text (to show it was already picked)
        self.buttons[index_1].configure(text="", state="disabled")
        self.buttons[index_2].configure(text="", state="disabled")

        # Append matched pair to the matches list.
        self.matches.append(self.cards[index_1])
        self.matches.append(self.cards[index_2])
        
        self.flipped_cards = [] # Empty the list
        self.is_processing = False  # Back to starting state
        
    def turn_back(self, index_1, index_2):
        """ A function that turns the cards back around after they do not match.
            
            Parameters: any of the initialized values, index_1 and index_2.
            Return: none.
        """
        # Return buttons to starting state (since the buttons were appended, the program remembers the images and positions).
        self.buttons[index_1].configure(image="", text="?") 
        self.buttons[index_2].configure(image="", text="?") 
        
        # Reset visibility
        self.cards[index_1].is_visible = False
        self.cards[index_2].is_visible = False
        
        self.flipped_cards = []  # Empty the list
        self.is_processing = False  # Back to starting state
        
    def quit_game(self):
        """ A function that makes the quit button and the reset button in a frame.
            
            Parameters: any of the initialized values.
            Return: none.
        """
        self.quit_frame.grid_columnconfigure(0, weight=1)
        self.quit_frame.grid_columnconfigure(3, weight=1)  # Create layout of frame
        quit_button = tk.Button(self.quit_frame, text="Abort Mission", fg="red", command=self.root.destroy)
        quit_button.grid(row=0, column=1, padx=10, pady=10)  # Place it in grid.
        self.buttons_frame.append(quit_button)  # Append to button list to remember.

        restart_button = tk.Button(self.quit_frame, text="Reset", fg="navy", command=self.restart_game)
        restart_button.grid(row=0, column=2, padx=10, pady=10)  # Place it in grid.
        self.buttons_frame.append(restart_button)  # Append to button list to remember.

    def restart_game(self):
        """ A function that makes the entire game restart (turns all cards to starting positions and reshuffles).
            
            Parameters: any of the initialized values.
            Return: none.
        """
        print("-----------------------------------------------------------------------------------------")
        print("The game has been reset.")
        self.flipped_cards = []  # Empty flip list if a turn was in progress
        self.matches = []
        self.is_processing = False 
            
        random.shuffle(self.files) # Reshuffle/reorder the list.
        self.cards = [Card(self.root, f) for f in self.files]   # Create a new card for each file.
        
        for i, button in enumerate(self.buttons): # Enumerate over the list containing the buttons
            button.configure(image="", text="?", state="normal")
            button.image = None
            button.configure(command=lambda c=self.cards[i], i=i: self.on_card_click(c, i))  # Assign the new card values to each button.

    def coordinate_entry(self):
        """ A function that makes the coordinate entry in a frame.
            
            Parameters: any of the initialized values.
            Return: none.
        """
        self.entry_frame.grid_columnconfigure(2, weight=1) 
        coord_label = tk.Label(self.entry_frame, text='Enter coordinates', fg='grey', bg='white', font=('Cambria', 10))
        coord_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.entry = tk.Entry(self.entry_frame)
        self.entry.grid(row=0, column=1, pady=5, columnspan=2, sticky='ew')  # Extend entry to entire frame.
        
        self.enter_button = tk.Button(self.entry_frame, text="Enter", fg="black", command=self.check_coordinates)
        self.enter_button.grid(row=0, column=3, pady=10)  # Place it in grid.
        self.buttons_frame.append(self.enter_button)  # Append to button list to remember.

    def check_coordinates(self):
        """ A function that checks the input coordinates.
            
            Parameters: any of the initialized values.
            Return: none.
        """
        if len(self.matches) >= 16:  # If all the matches are found.
            coordinates = self.entry.get()  # Get the entry
            if coordinates == "12015317018523790":
                self.enter_button.after(6000, self.root.destroy) # Quit game window
                messagebox.showinfo("Validating...", "Coordinates set. Target aquired. Rerouting..............."
                                    "\n\nRerouting complete. VIRGO11 will reach the Antennae in 71 Mly.")
                print("\nMission completed! The destination is set, please relax and wait for further instructions.")
                print("-----------------------------------------------------------------------------------------")
                print()
                print("THE END\n") 

            else:
                messagebox.showerror("Validating...", "Coordinates set. Target aquired. Rerouting..............."
                                    "\n\nReroute rejected. Target is not correct. \nPlease enter new coordinates or restart the mission.")
                print("Please restart the mission to obtain the correct coordinates")
                print("Press 'Reset' to immediately restart the matching process.")
                print("Press 'Abort Mission' to temporarily quit the mission. The matching process will then be retried at a later time.\n")
                  
# Main execution
if __name__ == "__main__": # Only run when the file is double-clicked or ran from terminal.
    Introduction("GalaxyM_Intro.txt")  # Call the introduction text.
    root = tk.Tk()  # Create main application window.
    root.withdraw()  # Immediatl withdraw window so it's not visible yet
    app = Game(root)  # Instance from the game, makes sure it starts.
    root.after(60000, lambda: root.deiconify())  # After 60000 milisec (1 min), show the window.
    root.mainloop()  # Keeps window open and waits for user interaction.


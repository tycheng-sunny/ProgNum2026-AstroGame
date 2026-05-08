#!/usr/bin/env python
# coding: utf-8

# In[17]:


import random #genenrating random numbers
import tkinter as tk #creates Graphical User Interface
from tkinter import messagebox #displays messages
from PIL import Image, ImageTk

class AstroMemo: #the main class
    def __init__(self, master, file_list): #this is to initialize the parameters and create the pairs
        self.master = master #main window 
        self.master.title("Match the Planets of our Solar System") #main window title
        
        # Grid and Size Settings
    
        self.button_size = 250  # We want 250 pixels
        
        # Setup files (8 pairs = 16 tiles)
        self.file_paths = file_list * 2
        random.shuffle(self.file_paths) #this randomizes the order
        
        self.buttons = [] #keeps track of all the buttons in the game
        self.clicked_buttons = [] #Keeps track on all the already clicked buttons
        self.images = {} 
        
        # Create a tiny 1x1 transparent pixel to force button size
        self.pixel = tk.PhotoImage(width=1, height=1)
        
        self.create_board() #creates the buttons in the game board

    def get_image(self, path):
        """Resizes the PNG to exactly 250x250 pixels."""
        if path not in self.images:
            img = Image.open(path)
            # Resizing to exactly 250x250
            img = img.resize((self.button_size, self.button_size), Image.Resampling.LANCZOS)
            self.images[path] = ImageTk.PhotoImage(img)
        return self.images[path]

    def create_board(self): #This makes the board
        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=20, pady=20)

        for i in range(4):#this way the go over the rows
            for j in range(4): #this way we go over the columns
                # Create button
                btn = tk.Button( #for each position we create a button
                    self.frame, 
                    bg="black", #the bakcground is black, like space
                    image=self.pixel, # We use the pixel to force pixel-based sizing
                    width=self.button_size, 
                    height=self.button_size,
                    compound="center", # Ensures image stays centered
                    borderwidth=0,     # Removes the gray frame
                    highlightthickness=0,
                    command=lambda r=i, c=j: self.flip(r, c) #lambda creates a anonymes function creates a function for the row and col (this is self. flip)
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(btn)

    def flip(self, row, col): #this makes the players able to flip the buttons
        index = row * 4 + col #calculates the index of the clicked button
        
        if self.buttons[index].cget("state") == "disabled" or len(self.clicked_buttons) >= 2: #condirions to check if the button shoor be flipped
            # first condition: ensures that the button has not already be flipped (than it is black)
            #the second one checks if not two buttons have already be clicked
            return
            #if both are not true, we get the image
        photo = self.get_image(self.file_paths[index])
        self.buttons[index].config(image=photo, state="disabled") #and after that put is as disabled
        self.clicked_buttons.append((index, self.file_paths[index])) #and add the index to the list clicked_buttons, to remember which one is clicked
        
        if len(self.clicked_buttons) == 2: #after flipping the button (the list if of clicked buttons is two)
            self.master.after(800, self.check_match) #After 800 ms, check if the two colors match

    def check_match(self): #this checks if the two flipped pictures match 
        idx1, path1 = self.clicked_buttons[0] #get the two clicked buttons
        idx2, path2 = self.clicked_buttons[1]
        
        if path1 == path2: #if the colors match
            self.clicked_buttons = [] #make the list empty again
            if all(btn.cget("state") == "disabled" for btn in self.buttons): #if all buttons are matched we get an message on screen
                messagebox.showinfo("Victory!", "You matched all the planets in our solar System!")
        else: #resets the colours if they do not match
            # Hide images again and put back the empty pixel
            self.buttons[idx1].config(image=self.pixel, state="normal") #otherwise return to the normal state (flipped state)
            self.buttons[idx2].config(image=self.pixel, state="normal")
            self.clicked_buttons = [] #And again clear the clicked Buttons list

def main(): #With this function we get all the pictures
    my_png_files = [
        "Mercury.png", "Venus.png", "Earth.png", "Mars.png",
        "Jupiter.png", "Saturn.png", "Uranus.png", "Pluto.png"
    ]
    
    root = tk.Tk()
    # Set a minimum window size so it doesn't jump around
    root.geometry("1100x1100") 
    
    AstroMemo(root, my_png_files)
    root.mainloop()

if __name__ == "__main__": #Start the loop
    main()


# In[ ]:





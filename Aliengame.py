#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pygame
import sys
import numpy as np
from astropy.io import fits

class Button:
    """
    A button that you can click class.
    """
    def __init__(self, x, y, width, height, text, font, bg_color, text_color, action):
        """
        Initializes the button with position, dimensions, text, styling and an action callback.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.action = action
        
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        """
        Draws the button rectangle and its text onto the given surface.
        """
        pygame.draw.rect(surface, self.bg_color, self.rect)
        surface.blit(self.text_surface, self.text_rect)

    def handle_event(self, event):
        """
        Checks if the button was clicked and triggers the assigned action if so.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action() 

# The game
class AlienGame:
    """
    Main game class that handles the Pygame window, assets, events and game loop.
    """
    def __init__(self):
        """
        Initializes Pygame, sets up the display, variables and loads game assets.
        """
        pygame.init()
        self.width = 600
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Alien Dress-Up")
        
        # Colors & fonts
        self.bg_color = (20, 20, 50)
        self.button_color = (100, 200, 100)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24) 
        
        # Game variables
        self.running = True
        self.hair_index = 0
        self.shirt_index = 0
        self.bg_image = None 
        
        # Setups
        self.load_assets()
        self.load_fits_data() 
        self.setup_buttons()

    def load_fits_data(self):
        """
        Reads astronomical data from the required FITS file.
        Extracts metadata for the fact text AND the raw pixel data for the background.
        """
        try:
            hdul = fits.open('m101.fits')
            header = hdul[0].header
            data = hdul[0].data
            
            obs_date = header.get('DATE-OBS', 'Unknown Date')
            target = header.get('OBJECT', 'Unknown Target')
            
            self.astro_fact = f"Telescope Target: {target} | Date: {obs_date}"
            
            if data is not None:
                data = np.nan_to_num(data)
                
                vmin, vmax = np.percentile(data, (1, 99.5))
                data_clipped = np.clip(data, vmin, vmax)
                
                data_norm = (data_clipped - vmin) / (vmax - vmin) * 255
                data_uint8 = data_norm.astype(np.uint8)
                
                data_transposed = data_uint8.T
                
                data_rgb = np.stack((data_transposed,) * 3, axis=-1)
                
                raw_bg = pygame.surfarray.make_surface(data_rgb)
                
                raw_bg = pygame.transform.flip(raw_bg, False, True)
                
                self.bg_image = pygame.transform.scale(raw_bg, (self.width, self.height))
                
            hdul.close()
            
        except FileNotFoundError:
            print("Could not find the FITS file! Make sure it is in the same folder.")
            self.astro_fact = "FITS Data Missing. Place file in directory."
        except Exception as e:
            print(f"Error reading FITS file: {e}")
            self.astro_fact = "Error reading FITS header data."

    def load_assets(self):
        """
        Loads all image assets for the alien and clothing options.
        """
        self.alien = pygame.image.load('alien.png')
            
        # Hair 
        purplehair = pygame.image.load('purplehair.png')
        bluehair = pygame.image.load('bluehair2.png')
        greenhair = pygame.image.load('greenhair.png')
        self.hair_options = [None, purplehair, bluehair, greenhair]
            
        # Shirts
        shirt1 = pygame.image.load('ufoshirt.png')
        shirt2 = pygame.image.load('starsshirt.png')
        shirt3 = pygame.image.load('ilovecodingshirt.png')
        self.shirt_options = [None, shirt1, shirt2, shirt3]
            

    def setup_buttons(self):
        """
        Creates the buttons and maps them to their respective click functions.
        """
        self.buttons = []
        
        hair_btn = Button(50, 600, 220, 50, "Change hair", self.font, 
                          self.button_color, self.text_color, self.cycle_hair)
        self.buttons.append(hair_btn)
        
        shirt_btn = Button(300, 600, 220, 50, "Change shirt", self.font, 
                           self.button_color, self.text_color, self.cycle_shirt)
        self.buttons.append(shirt_btn)

    def cycle_hair(self):
        """
        Cycles to the next hair option in the list. Loops back to the start if at the end.
        """
        self.hair_index += 1
        if self.hair_index >= len(self.hair_options):
            self.hair_index = 0

    def cycle_shirt(self):
        """
        Cycles to the next shirt option in the list. Loops back to the start if at the end.
        """
        self.shirt_index += 1
        if self.shirt_index >= len(self.shirt_options):
            self.shirt_index = 0

    def handle_events(self):
        """
        Processes standard Pygame events like quitting and passes mouse clicks to buttons.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Let every button check if it was clicked
            for button in self.buttons:
                button.handle_event(event)

    def draw(self):
        """
        Renders the background, alien, current clothing, FITS data, and buttons to the screen.
        """
        # Drawbackground
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill(self.bg_color)
        
        if hasattr(self, 'astro_fact'):
            fact_surface = self.small_font.render(self.astro_fact, True, (255, 255, 150))
            self.screen.blit(fact_surface, (20, 20))

        # Alien Base
        if self.alien:
            self.screen.blit(self.alien, (100, 50))
            
        # Draw Shirt
        current_shirt = self.shirt_options[self.shirt_index]
        if current_shirt:
            self.screen.blit(current_shirt, (100, 50))
            
        # Draw Hair
        current_hair = self.hair_options[self.hair_index]
        if current_hair:
            self.screen.blit(current_hair, (100, 50))
            
        # Draw Buttons
        for button in self.buttons:
            button.draw(self.screen)
            
        pygame.display.flip()

    def run(self):
        """
        The main game loop that continuously handles events and redraws the screen.
        """
        while self.running:
            self.handle_events()
            self.draw()
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = AlienGame()
    game.run()


# In[ ]:





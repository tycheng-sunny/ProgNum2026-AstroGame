#!/usr/bin/env python3

#if the code doesn't work, you may have to install pygame (pip install pygame) 
#- same for astroquery

#BLACK HOLE GAME: inspired by pacman - player uses arrow keys to steer their black hole and eat stars, gathering their mass
#user can eat other black holes as long as their black hole has bigger mass
#other black holes are like ghosts in pacman - they can eat you!
#Win when user absorbs all black holes or stars, or has the most mass of all objects

import pygame #used for the game to open in a seperate window (fun:))
import random
import math
from astroquery.vizier import Vizier #bright nearby stars

pygame.init() #starts the game, window opens:)

#game screen
WIDTH, HEIGHT = 800, 800 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Black Hole Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)


#creating classes: (will be used later!)
#Player (with movement function)
class Player:
    """user's black hole"""
    def __init__(self, x, y, username):
        self.x = x
        self.y = y
        self.mass = 0 #starts out with mass 0
        self.speed = 5
        self.username = username

    def move(self, keys): #movement of player
        if keys[pygame.K_LEFT]: #according to arrow keys
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

#Ghosts:
class Ghost:
    """black holes corresponding to ghosts in pacman"""
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
        self.speed = 0.5

    def chase(self, player): #movement of ghosts; chases player
        #ghost movement towards player
        dx = player.x - self.x
        dy = player.y - self.y

        #normalize direction --> speed = const
        dist = math.sqrt(dx**2 + dy**2) #direction
        
        if dist != 0:
            dx /= dist
            dy /= dist #direction vector into unit vector so that speed=const
     
        #coords
        self.x += dx * self.speed
        self.y += dy * self.speed

#Food:
class Food:
    """stars from astroquery"""
    def __init__(self, x, y, mass, name):
        self.x = x
        self.y = y
        self.mass = mass
        self.name = name


#defining useful functions:   
def distance(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

def draw_text(text, x, y):
    img = font.render(text, True, (255, 255, 255))
    screen.blit(img, (x, y))

#MENU
#the game starts with the 'menu' page - game title and username input
state = "MENU" 
username = ""
#note: states (state="MENU" or state="PLAY" controls whether program is in menu or the game

#placeholders before game starts:
player = None
foods = []
ghosts = []

#astronomical data for stars (food):
Vizier.ROW_LIMIT = 20
result = Vizier.query_constraints(catalog="V/50", Vmag="<6") #stars brighter than max=6
stars = result[0]


#running of the game
running = True

while running:
    screen.fill((0, 0, 0))

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #this part here lets us type
            running = False
            
    #Menu
        if state == "MENU":
            if event.type == pygame.KEYDOWN: #aka when key pressed once
                if event.key == pygame.K_RETURN: #when ENTER pressed
                    state = "PLAY" #the game goes to PLAY

                    #objects:
                    player = Player(WIDTH // 2, HEIGHT // 2, username)
                    
                    foods = [] #celestial bodies -> food for user's black hole
                    for i in range(len(stars)):
                        name = str(stars["Name"][i]) if "Name" in stars.colnames else f"Star-{i}"

                        #in catalogue no mass, so the mass used for game will be converted from brightness
                        mag = stars["Vmag"][i]
                        mass = max(1, int(10-mag)) #NOTE! this is game mass!
    
                        foods.append(Food(random.randint(0, WIDTH), random.randint(0, HEIGHT), mass, name))

                    
                    ghost_positions = [
                        (50, 50),                     # top-left
                        (WIDTH - 50, 50),             # top-right
                        (50, HEIGHT - 50),            # bottom-left
                    ]
                    
                    ghosts = []   
                    for p in ghost_positions:
                        ghosts.append(Ghost(p[0], p[1], random.randint(25, 45)))
                        

                    
                elif event.key == pygame.K_BACKSPACE: #input for username
                    username = username[:-1]
                else:
                    username += event.unicode #+typed character to username string (keyboard input)


    #Menu screen:
    if state == "MENU":
        draw_text("BLACK HOLE GAME", 300, 180)
        draw_text("Enter username: " + username, 300, 470)
        #game explenation:
        draw_text("Use arrow keys to move the black hole!", 150, 300)
        draw_text("Eat the stars to gain mass and avoid bigger black holes;", 150, 330)
        draw_text("You can eat another black hole once yours has the bigger mass!", 150, 360)
        draw_text("To win eat all black holes or stars, or gain biggest mass", 150, 390)
        #about data:
        draw_text("Disclaimer:", 100,530)
        draw_text("Data used for star names and masses is imported from astroquery.vizier...", 100, 550)
        draw_text("The star masses used in the game does not correspond to real life masses!", 100, 570)
        draw_text("It is arbitrary and comes from the stars' apparent magnitudes:)", 100, 590)
        draw_text("(m = 10 - magnitude)", 280, 610)
        pygame.display.flip()
        clock.tick(60)
        continue


    #FINALLY game logic
    #movement (using the arrow keys!)
    if state == "PLAY":
        keys = pygame.key.get_pressed()
        player.move(keys)
    
        #Visuals:
           
        #visuals of the player:
        pygame.draw.circle(screen, (200, 0, 200), (player.x, player.y), 15)
        draw_text(f"{player.username}: {player.mass}", player.x - 30, player.y - 30)

        #drawing the food:
        for food in foods[:]:
            pygame.draw.circle(screen, (255, 255, 0), (food.x, food.y), 8)
            draw_text(f"{food.name}: {food.mass}", food.x, food.y)
            #eating:
            if distance(player, food) < 20:
                player.mass += food.mass
                foods.remove(food)

        for ghost in ghosts[:]:
            ghost.chase(player)
        
            #the actual visual:)
            pygame.draw.circle(screen, (255, 0, 0), (ghost.x, ghost.y), 18)
            draw_text(f"black hole: {ghost.mass}", ghost.x, ghost.y)

            # collision
            if distance(player, ghost) < 25: #adding mass of food to player due to proximity (collision)
                if player.mass > ghost.mass:
                    player.mass += ghost.mass
                    ghosts.remove(ghost)
                    break
                else:
                    print("GAME OVER")
                    running = False

    
        #Win conditions
        if len(ghosts) == 0: #if you eat all ghosts
            print("YOU WIN!")
            running = False

        if len(foods) == 0: #if you eat all stars
            print("YOU WIN!")
            running = False

        all_masses = [food.mass for food in foods] + [ghost.mass for ghost in ghosts]
        if player.mass > max(all_masses, default=0):
            print("YOU WIN!")
            running = False #if player's mass bigger than all others

        pygame.display.flip()
        clock.tick(60)

pygame.quit() #game ends, window closes
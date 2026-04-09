from astropy.io import fits
import pygame
from pygame.locals import *
import sys
import numpy as np

# initialize pygame
pygame.init()

# setting up colors
black = pygame.Color(0, 0, 0)         
white = pygame.Color(255, 255, 255)   
blue = pygame.Color(0, 0, 255) 
red = pygame.Color(255, 0, 0)  
grey = pygame.Color(80, 80, 80)

# screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Create (x,y) screen coordinates from ra and dec.
hdul = fits.open('astroquery_gaia.fits')
data = hdul[1].data
x = data['ra'] / 360 * screen_width
y = (screen_height/2) + (data['dec'] / 90 * (screen_height/2))

mag = data['phot_g_mean_mag']
min_mag, max_mag = np.min(mag), np.max(mag)
# normalize (0 = faintest, 1 = brightest)
norm = (max_mag - mag) / (max_mag - min_mag)
# scale to radius range
radius = 1 + norm * 4 # gives sizes 1–5

# game-over text font
font = pygame.font.Font(None, 36)

class Player():
    def __init__(self):
        # player image and location
        self.image = pygame.image.load("p1.png")
        self.rect = self.image.get_rect()
        self.rect.center=(100, 40)

        # player stats / starting variables
        self.speed = 5
        self.acquired_sunglasses = False 
        self.sunglasses = False
        self.next_mission = False
        self.xp = 0
        self.gameover = False

    def update(self, surface):
        '''Draws player and moves player around on surface based on WASD keyboard keys input'''
        surface.blit(self.image, self.rect)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_w]:
            self.rect.top -= self.speed
        if pressed_keys[K_s]:
            self.rect.top += self.speed
        if pressed_keys[K_a]:
                self.rect.left -= self.speed
        if pressed_keys[K_d]:
                self.rect.left += self.speed

    def set_sunglasses(self):
        '''Player puts sunglasses on/off if sunglasses are acquired'''
        if self.sunglasses==False and self.acquired_sunglasses:
            self.image = pygame.image.load("p2.png") # image with sunglasses
            self.sunglasses = True
        elif self.sunglasses:
            self.image = pygame.image.load("p1.png") # image without sunglasses
            self.sunglasses = False

    def game_over(self):
        '''Player is dead and can't move around anymore'''
        self.image = pygame.image.load("p3.png")
        self.speed = 0
        self.gameover = True

class Bullet():
    def __init__(self, xy, speed):
        self.image = pygame.Surface((8, 8))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.speed = speed

    def update(self, surface):
        '''Draws and updates the bullets on the surface'''
        surface.blit(self.image, self.rect)
        self.rect.centerx += self.speed

class Enemy():
    def __init__(self):
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center=(np.random.randint(20, screen_width-20), np.random.randint(20, screen_height-20))

    def movement(self, x, y):
        '''Enemy moves toward input coordinates x and y with a speed of 2'''
        speed = 2
        if self.rect.centerx < x: self.rect.centerx += speed
        else: self.rect.centerx -= speed
        if self.rect.centery < y: self.rect.centery += speed
        else: self.rect.centery -= speed

    def update(self, surface, x, y):
        '''Update and draw enemy location on surface, enemy will move towards input x and y coordinates'''
        self.movement(x, y)
        surface.blit(self.image, self.rect)

# creating player and defining starting variables
p1 = Player()
enemies = []
bullets = []
bullet_speed = 10
clock = pygame.time.Clock()
while True:
    clock.tick(60) # limits frames per second to 60
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==KEYDOWN:
            if event.key==K_e:
                p1.set_sunglasses()
            if event.key==K_a: bullet_speed = -10
            if event.key==K_d: bullet_speed = 10
            if event.key==K_SPACE and p1.sunglasses == False:
                bullets.append(Bullet(p1.rect.center, bullet_speed))

    # Mission 1: acquire sunglasses
    if p1.acquired_sunglasses == False:
        screen.blit(pygame.image.load("sunglass.png"), (750, 300))
        diff = 30
        # if close enough to sunglasses -> acquire sunglasses and trigger new mission
        if p1.rect.centerx > 750 - diff and p1.rect.centerx < 750 + diff and p1.rect.centery > 300 - diff and p1.rect.centery < 300 + diff:
            p1.acquired_sunglasses = True
            p1.next_mission = True

    # Draw stars
    if p1.next_mission:
        mission_i = np.random.randint(len(data))
        p1.next_mission = False
    for i in range(len(data)):
        if p1.sunglasses and i==mission_i: 
            pygame.draw.circle(screen, blue, (x[i], y[i]), int(radius[i])+3) # mission star has blueish glow with sunglasses on
        if p1.sunglasses: star_color = grey # stars appear grey with sunglasses on
        else: star_color = white
        pygame.draw.circle(screen, star_color, (x[i], y[i]), int(radius[i]))

    # Enemy randomly spawning, chance that they spawn increases with 0.1% for every 15 xp
    if np.random.randint(0, 1000) >= 997 - p1.xp//15:
        enemies.append(Enemy())
    # Draw enemies & check if they collide with player -> game_over
    for e in enemies:
        e.update(screen, p1.rect.centerx, p1.rect.centery)
        if p1.rect.colliderect(e.rect):
            p1.game_over()
            enemies = []

    # Bullets logic
    for b in bullets:
        b.update(screen)
        if b.rect.centerx > screen_width:
            bullets.remove(b)
        for e in enemies:
            # check bullet and enemy collisions
            if b.rect.colliderect(e.rect):
                pygame.draw.circle(screen, red, e.rect.center, 20)
                bullets.remove(b)
                enemies.remove(e)
                break

    p1.update(screen)
    # check if player is nearby a star
    for i in range(len(data)):
         diff = 35
         if p1.rect.centerx > x[i] - diff and p1.rect.centerx < x[i] + diff and p1.rect.centery > y[i] - diff and p1.rect.centery < y[i] + diff:
            # check if player is at the mission star and wearing sunglasses
            if p1.sunglasses and i==mission_i:
                p1.next_mission = True
                p1.xp += 1
            elif p1.sunglasses:
                pygame.draw.circle(screen, white, (x[i], y[i]), 5) # nearby stars become white
            else: screen.fill(grey) # screen becomes grey / player becomes temporarily blind

    # game_over message on screen
    if p1.gameover:
        text = font.render(f'Data gathered from: {p1.xp} stars', True, white)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)
    pygame.display.update()
    
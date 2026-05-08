#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pygame
import random
import math
import numpy as np
from astropy.io import fits

WIDTH, HEIGHT = 800, 600
FPS = 60
ATOM_COUNT = 10
BG_COLOR = (10, 10, 20)
NUCLEUS_COLOR = (255, 50, 50)
ELECTRON_COLOR = (50, 150, 255)
ORBIT_COLOR = (50, 50, 50)
PHOTON_COLOR = (255, 255, 0)
THRESHOLD_FREQUENCY = 10 

def load_fits_to_surface():
    '''Converts the M101 FITS data into a Pygame surface'''
    try:
        hdul = fits.open('m101.fits')
        dat = hdul[0].data
        dat_min, dat_max = np.min(dat), np.max(dat)
        dat_normalized = ((dat - dat_min) / (dat_max - dat_min) * 255).astype(np.uint8)
        surf = pygame.Surface((530, 530))
        rgb_dat = np.stack([dat_normalized]*3, axis=-1)
        pygame.surfarray.blit_array(surf, np.transpose(rgb_dat, (1, 0, 2)))
        return pygame.transform.scale(surf, (int(WIDTH * 0.8), int(HEIGHT * 0.8)))
    except Exception as e:
        print(f"Could not load FITS: {e}")
        fallback = pygame.Surface((int(WIDTH * 0.8), int(HEIGHT * 0.8)))
        fallback.fill((50, 0, 50))
        return fallback

class Photon:
    def __init__(self, x, y, frequency):
        '''Determines Photon Properties'''
        self.x, self.y = x, y
        self.frequency = frequency
        self.speed = 10
        self.radius = 3
        self.active = True

    def update(self):
        '''Determines the motion of the photon'''
        self.x += self.speed
        if self.x > WIDTH: self.active = False

    def draw(self, surface):
        '''Draws Photon'''
        pygame.draw.circle(surface, PHOTON_COLOR, (int(self.x), int(self.y)), self.radius)

class HydrogenAtom:
    def __init__(self):
        self.reset()
        
    def reset(self):
        '''Determiens the properties of the Hydrogen atom'''
        self.x = random.randint(200, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        self.orbit_radius = random.randint(30, 50)
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(0.02, 0.05)
        self.nucleus_size, self.electron_size = 8, 4
        self.is_ionized = False
        self.e_x, self.e_y, self.e_vx, self.e_vy = 0, 0, 0, 0

    def update(self, photons):
        '''Determines the movement of photons and electrons and their interaction'''
        if not self.is_ionized:
            self.angle += self.speed
            self.e_x = self.x + self.orbit_radius * math.cos(self.angle)
            self.e_y = self.y + self.orbit_radius * math.sin(self.angle)
            for p in photons:
                if math.hypot(self.e_x - p.x, self.e_y - p.y) < 15:
                    if p.frequency >= THRESHOLD_FREQUENCY:
                        self.ionize()
                        p.active = False
        else:
            self.e_x += self.e_vx
            self.e_y += self.e_vy

    def ionize(self):
        '''Determines the trajectory of the electron following ionization'''
        self.is_ionized = True
        mag = 7 
        self.e_vx, self.e_vy = -math.sin(self.angle) * mag, math.cos(self.angle) * mag

    def draw(self, surface):
        '''Draws the particles'''
        if not self.is_ionized:
            pygame.draw.circle(surface, ORBIT_COLOR, (self.x, self.y), self.orbit_radius, 1)
        pygame.draw.circle(surface, NUCLEUS_COLOR, (self.x, self.y), self.nucleus_size)
        pygame.draw.circle(surface, ELECTRON_COLOR, (int(self.e_x), int(self.e_y)), self.electron_size)

def main():
    '''The game itself'''
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Times New Roman", 48)
    m101_surface = load_fits_to_surface()
    m101_rect = m101_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
    try:
        user_freq = float(input("Enter Photon Frequency (Threshold 10): "))
    except:
        user_freq = 5
    atoms = [HydrogenAtom() for _ in range(ATOM_COUNT)]
    photons = []
    
    flash_timer = 0
    show_image = False
    
    running = True
    game_over = False

    while running:
        screen.fill(BG_COLOR)
        dt = clock.tick(FPS)     
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False        
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                m_x, m_y = pygame.mouse.get_pos()
                photons.append(Photon(m_x + 10, m_y, user_freq))
                if random.randint(1, 10) == 1:
                    show_image = True
                    flash_timer = 100 
        if not game_over:
            for p in photons[:]:
                p.update()
                p.draw(screen)
                if not p.active: photons.remove(p)
            all_ionized = True
            for atom in atoms:
                atom.update(photons)
                atom.draw(screen)
                if not atom.is_ionized: all_ionized = False
            if show_image:
                screen.blit(m101_surface, m101_rect)
                flash_timer -= dt
                if flash_timer <= 0:
                    show_image = False
            if all_ionized: game_over = True
        else:
            screen.fill((0, 0, 0))
            txt = font.render("You're winner", True, (255, 255, 255))
            screen.blit(txt, txt.get_rect(center=(WIDTH//2, HEIGHT//2)))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()


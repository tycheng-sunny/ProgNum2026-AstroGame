# Entities/Playercode.py
import pygame
import os
from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_DOWN

class player:
    def __init__(self, pos, size, screen_width=1080, screen_height=720):
        self.pos = pos
        self.size = size  # tamaño visual en pantalla (escalado)
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Cargar la imagen de la nave y escalarla al tamaño deseado
        img_path = os.path.join(os.path.dirname(__file__), "..", "ship.png")
        raw = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(raw, (self.size[0], self.size[1]))

        # Radio de colisión: 40% del lado más pequeño, ajustado a la silueta real
        self.collision_radius = min(self.size[0], self.size[1]) * 0.40

    def movement(self, pspeed):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[K_LEFT]:
            dx -= 1
        if keys[K_RIGHT]:
            dx += 1
        if keys[K_UP]:
            dy -= 1
        if keys[K_DOWN]:
            dy += 1

        length = (dx**2 + dy**2)**0.5
        if length != 0:
            dx /= length
            dy /= length

        self.pos[0] += dx * pspeed
        self.pos[1] += dy * pspeed

        self.pos[0] = max(0, min(self.pos[0], self.screen_width - self.size[0]))
        self.pos[1] = max(0, min(self.pos[1], self.screen_height - self.size[1]))

    def check_collision(self, asteroid):
        # Colisión círculo-círculo: centro de la nave vs centro del asteroide
        center_x = self.pos[0] + self.size[0] / 2
        center_y = self.pos[1] + self.size[1] / 2
        distance = ((center_x - asteroid.pos[0])**2 + (center_y - asteroid.pos[1])**2)**0.5
        return distance < asteroid.radius + self.collision_radius

    def draw(self, screen):
        screen.blit(self.image, (int(self.pos[0]), int(self.pos[1])))
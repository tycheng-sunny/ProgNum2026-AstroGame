# Entities/AsteroidCode.py
import pygame
import random
import math
import os

# Imagen compartida entre todas las instancias (se carga una sola vez)
_asteroid_image = None
_asteroid_image_ring = None

def _remove_white_bg(surface, threshold=240):
    """Convierte píxeles blancos/casi blancos en transparentes (flood fill desde bordes)."""
    surface = surface.convert_alpha()
    w, h = surface.get_size()
    visited = set()
    stack = [(x, y) for x in range(w) for y in [0, h-1]] + \
            [(x, y) for y in range(h) for x in [0, w-1]]
    while stack:
        x, y = stack.pop()
        if (x, y) in visited or not (0 <= x < w and 0 <= y < h):
            continue
        visited.add((x, y))
        r, g, b, a = surface.get_at((x, y))
        if r > threshold and g > threshold and b > threshold:
            surface.set_at((x, y), (0, 0, 0, 0))
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                stack.append((x+dx, y+dy))
    return surface

def _load_images():
    global _asteroid_image, _asteroid_image_ring
    if _asteroid_image is None:
        path = os.path.join(os.path.dirname(__file__), "..", "asteroid.png")
        raw = _remove_white_bg(pygame.image.load(path))
        _asteroid_image = raw

        # Teñir de rojo solo los píxeles opacos, dejando transparentes intactos
        ring = raw.copy()
        w, h = ring.get_size()
        for y in range(h):
            for x in range(w):
                r, g, b, a = ring.get_at((x, y))
                if a > 0:
                    ring.set_at((x, y), (min(255, r + 80), max(0, g - 40), max(0, b - 40), a))
        _asteroid_image_ring = ring

class Asteroid:
    def __init__(self, screen_width, target_pos=None, spawn_pos=None):
        self.screen_width = screen_width
        self.radius = random.randint(10, 30)
        self.speed = random.randint(2, 6)
        self.is_ring_asteroid = spawn_pos is not None

        if spawn_pos is not None:
            self.pos = list(spawn_pos)
        else:
            self.pos = [random.randint(0, screen_width), random.randint(0, 3)]

        if target_pos is not None:
            dx = target_pos[0] - self.pos[0]
            dy = target_pos[1] - self.pos[1]
            dist = math.sqrt(dx**2 + dy**2)
            self.direction = (dx / dist, dy / dist) if dist > 0 else (0, 1)
        else:
            self.direction = (0, 1)

        # Escalar la imagen al diámetro de este asteroide
        _load_images()
        diameter = self.radius * 2
        base = _asteroid_image_ring if self.is_ring_asteroid else _asteroid_image
        self.image = pygame.transform.scale(base, (diameter, diameter))

    def update(self, screen_width, screen_height):
        self.pos[0] += self.direction[0] * self.speed
        self.pos[1] += self.direction[1] * self.speed

        if not self.is_ring_asteroid:
            if (self.pos[1] > screen_height or self.pos[1] < 0 or
                    self.pos[0] < 0 or self.pos[0] > screen_width):
                self.pos[1] = random.randint(0, 3)
                self.pos[0] = random.randint(0, screen_width)

    def draw(self, screen):
        draw_x = int(self.pos[0]) - self.radius
        draw_y = int(self.pos[1]) - self.radius
        screen.blit(self.image, (draw_x, draw_y))
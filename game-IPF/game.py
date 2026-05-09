#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
asteroid_evader.py
==================
Astronomy-themed asteroid evasion game for a university project.
Requires: pip install pygame

Controls:
  A / D arrow keys         →  move the spaceship
  R                        →  restart after Game Over
  ESC                      →  quit game
"""

import pygame
import random
import sys
import math

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SCREEN_W, SCREEN_H = 800, 600
FPS = 60
FONT_SIZE = 22     # height of text in pixels

# Each level defines a celestial body and its real gravitational acceleration
# (m/s²).  We scale g by GRAVITY_SCALE so the on-screen fall feels playable
# while still preserving the relative differences between bodies.
GRAVITY_SCALE = 8          # pixels-per-second^2 per 1 m/s^2 of real gravity

# "color" key determines color of the display in the top left corner
# "bg" key determines the background color: the color of each planets atmosphere
LEVELS = [
    {"name": "Moon",    "g": 1.62,  "color": (200, 200, 210), "bg": (10, 10, 30)},
    {"name": "Earth",   "g": 9.81,  "color": (100, 180, 100), "bg": (5,  20, 50)},
    {"name": "Neptune", "g": 11.15, "color": (80,  120, 200), "bg": (0,  10, 40)},
    {"name": "Jupiter", "g": 24.79, "color": (210, 160,  80), "bg": (20, 10, 10)},
]

# Difficulty ramps: how many asteroids spawn per second at each level
SPAWN_RATES = [1, 2, 4, 8]   # asteroids / second (index matches LEVELS)

# Surival time (in seconds) needed to pass each level
TIME_PER_LEVEL = 15


# ---------------------------------------------------------------------------
# Spaceship class
# ---------------------------------------------------------------------------
class Spaceship:
    """Represents the player-controlled spaceship at the bottom of the screen."""

    WIDTH  = 50
    HEIGHT = 30
    SPEED  = 4   # pixels per frame

    def __init__(self):
        """Initialise the ship centred horizontally near the bottom."""
        self.x = SCREEN_W // 2 - self.WIDTH // 2  # Half of screen width subtracted with half of spaceship width to center spaceship 
        self.y = SCREEN_H - self.HEIGHT - 10      # Placing the spaceship at the bottom of the screen with a 10 pixel gap
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)     # Rectangular object for tracking the spaceships position and size: essentially the spaceship's hitbox

    def move(self, keys):
        """Update horizontal position based on keyboard input."""
        # K_a is the A key, K_d the D key on the keyboard fo the computer
        # The second part of the if condition is to prevent the spaceship going off-screen
        if keys[pygame.K_a] and self.rect.left  > 0:
            self.rect.x -= self.SPEED
        if keys[pygame.K_d] and self.rect.right < SCREEN_W:
            self.rect.x += self.SPEED

    def draw(self, surface):
        """Draw a layered cartoon spaceship. This is purely for decoration purposes"""
        r = self.rect
    
        # Defining the wing shape (a wider base triangle behind the main body)
        wings_points = [
            (r.centerx, r.top + 5),    # Point of the triangle
            (r.left, r.bottom),        # Bottom-left corner of the ship's boundary
            (r.right, r.bottom)        # Bottom-right corner of the ship's boundary
        ]
        pygame.draw.polygon(surface, (0, 150, 200), wings_points) # "Drawing" the triangle with a dark blue color: (0, 150, 200)
    
        # Defining the main Fuselage (the central "rocket" body)
        body_width = r.width * 0.6
        body_points = [
            (r.centerx, r.top),                    # Sharper point
            (r.centerx - body_width//2, r.bottom), # Bottom left of body
            (r.centerx + body_width//2, r.bottom)  # Bottom right of body
        ]
        pygame.draw.polygon(surface, (0, 220, 255), body_points) # "Drawing" the triangle with a blue color (0, 220, 255)
    
        # Adding a cockpit: a small circle or oval near the top
        cockpit_pos = (r.centerx, r.top + r.height // 3)
        pygame.draw.circle(surface, (200, 255, 255), cockpit_pos, 4)
    
        # Adding "engine glow": a large outer orange glow
        pygame.draw.circle(surface, (255, 140, 0), r.midbottom, 8)
        # Small inner yellow core
        pygame.draw.circle(surface, (255, 255, 0), r.midbottom, 4)


# ---------------------------------------------------------------------------
# Asteroid class
# ---------------------------------------------------------------------------
class Asteroid:
    """A single falling asteroid whose speed increases under gravity."""

    def __init__(self, gravity_px: float):
        """Spawn the asteroid at a random horizontal position at the top."""
        self.radius = random.randint(10, 50)  # Random radius of asteroid
        self.x = random.randint(self.radius, SCREEN_W - self.radius)  # random x-coordinate spawning position
        self.y = -self.radius               # Spawns asteroid just above the screen for continuity
        self.vy = random.uniform(60, 130)   # Random vertical starting velocity (pxels / second)
        self.gravity = gravity_px           # Corresponding asteroid acceleration for current level

        # Possible asteroid color:
        self.color = (random.randint(100, 140),
                      random.randint(70, 100),
                      random.randint(60,  70)) 
        
        # Create a "jagged" shape by picking 8-12 points around a circle
        self.points = []
        num_points = random.randint(8, 12)  # Amount of corners
        for i in range(num_points):
            angle = (i / num_points) * 2 * 3.14159 # 360 degrees in radians
            # Vary the distance from the center slightly for each point
            dist = self.radius * random.uniform(0.7, 1.1)    # Wobbling the distance: the distance between the edge and the center of the asteroid is random uniform
            # Converting to standard Carthesian coordinates:
            px = math.cos(angle) * dist    
            py = math.sin(angle) * dist
            self.points.append((px, py))   #Saving local offsets; coordinate are relative to the center of the asteroid

    def update(self, dt: float):
        """Apply gravitational acceleration and move down by one time-step.

        Args:
            dt: elapsed time since last frame in seconds.
        """
        self.vy += self.gravity * dt   # v = v₀ + g·t  (Newtonian kinematics): making the asteroid accelerate
        self.y  += self.vy    * dt     # y = y₀ + v·t : updating the vertical position based on the previous defined speed

    # Creating a detectable hitbox around the asteroids
    @property
    def rect(self) -> pygame.Rect:
        """Return a bounding rectangle used for collision detection."""
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2,       self.radius * 2)

    # Deleting asteroids that go offscreen to prevent lag
    def is_off_screen(self) -> bool:
        """Return True once the asteroid has fallen below the visible area."""
        return self.y - self.radius > SCREEN_H

    # Making the asteroids visable in the game
    def draw(self, surface):
        """Draw the asteroid as a jagged polygon."""
        # Calculating the actual screen positions for the points
        screen_points = [(int(self.x + px), int(self.y + py)) for px, py in self.points]
        
        # Drawing the rock body
        pygame.draw.polygon(surface, self.color, screen_points)
        # Draw a darker outline to make it pop
        pygame.draw.polygon(surface, (50, 50, 50), screen_points, 2)


# ---------------------------------------------------------------------------
# Game class
# ---------------------------------------------------------------------------
class Game:
    """Manages the main game loop, level progression, and rendering."""

    def __init__(self):
        """Initialise pygame, create the window, and reset game state."""
        pygame.init()    # "Turns on" internal Pygame modules
        self.screen  = pygame.display.set_mode((SCREEN_W, SCREEN_H))  # Creating the window used for the game
        pygame.display.set_caption("Asteroid Evader")
        self.font   = pygame.font.SysFont(None, FONT_SIZE)   # HUD font
        self.ticker  = pygame.time.Clock()                   # Making the game run at the same speed on different computers
        self.reset()      # Calling the reset function to start the game

    def reset(self):
        """Reset all game state to start a fresh game from level 0."""
        self.level_index  = 0            # Starts player at the first level
        self.score        = 0.0          # Accumulates over time (points/s)
        self.asteroids    = []           # New asteroids objects are appende din this list
        self.spawn_timer  = 0.0          # Seconds since last spawn
        self.ship         = Spaceship()  # Creates new spaceship
        self.game_over    = False 

    # ------------------------------------------------------------------
    # Properties that read from the current level dict
    # ------------------------------------------------------------------
    @property
    def current_level(self) -> dict:
        """Return the dict describing the current celestial body."""
        return LEVELS[self.level_index]

    @property
    def gravity_px(self) -> float:
        """Real g (m/s²) scaled to pixels/s² for use in physics."""
        return self.current_level["g"] * GRAVITY_SCALE

    # ------------------------------------------------------------------
    # Core loop helpers
    # ------------------------------------------------------------------
    def handle_events(self):
        """Process OS and keyboard events; return False to quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:     # Case: pressing x at top right
                return False
            if event.type == pygame.KEYDOWN:      # Case: pressing button
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_r and self.game_over:
                    self.reset()    # restart on 'R' after game over
        return True

    def spawn_asteroids(self, dt: float):
        """Spawn new asteroids at the rate defined for the current level.

        Args:
            dt: elapsed time in seconds since last frame.
        """
        self.spawn_timer += dt          # "Stopwatch"
        interval = 1.0 / SPAWN_RATES[self.level_index]   # "Seconds between spawns"
        while self.spawn_timer >= interval:
            self.asteroids.append(Asteroid(self.gravity_px))  # Append a new asteroid to the list defined in the class "Game"
            self.spawn_timer -= interval    # Reset stopwatch

    def update(self, dt: float):
        """Update all game objects, check collisions, and advance levels.

        Args:
            dt: elapsed time in seconds since last frame.
        """
        # Stops the game from spawning new objects when "game over"
        if self.game_over:
            return

        # Move the player ship
        self.ship.move(pygame.key.get_pressed())

        # Spawn, update, and cull asteroids
        self.spawn_asteroids(dt)
        for ast in self.asteroids:
            ast.update(dt)
        self.asteroids = [a for a in self.asteroids if not a.is_off_screen()]

        # Collision detection: axis-aligned bounding-box overlap
        for ast in self.asteroids:
            if self.ship.rect.colliderect(ast.rect):
                self.game_over = True
                return

        # Score increases with time survived (scaled by gravity for challenge)
        self.score += dt

        # Advance level when score threshold is reached and a next level exists
        if self.score >= TIME_PER_LEVEL * (self.level_index + 1):
            if self.level_index < len(LEVELS) - 1:
                self.level_index += 1
                #self.asteroids.clear()
                self.spawn_timer = 0.0

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def draw_hud(self):
        """Render the Heads-Up Display showing level, gravity, and score."""
        lvl  = self.current_level
        # Left side: level name and real gravity value
        label_level   = self.font.render(
            f"Level {self.level_index + 1}: {lvl['name']}", True, (255, 255, 255))
        label_gravity = self.font.render(
            f"Gravity: {lvl['g']:.2f} m/s^2", True, lvl["color"])
        label_score   = self.font.render(
            f"Score: {int(self.score)}", True, (220, 220, 100))

        # Draws the previously defined labels in top left corner
        self.screen.blit(label_level,   (10, 10))
        self.screen.blit(label_gravity, (10, 36))
        self.screen.blit(label_score,   (10, 62))

        # Thin coloured bar along the top to distinguish levels visually
        pygame.draw.rect(self.screen, lvl["color"], (0, 0, SCREEN_W, 4))

    def draw_game_over(self):
        """Display a centred Game Over message with the final score."""
        big_font  = pygame.font.SysFont(None, 64)
        small_font = pygame.font.SysFont(None, 32)
        msg1 = big_font.render("GAME OVER", True, (255, 60, 60))
        msg2 = small_font.render(f"Score: {int(self.score)}  |  Press R to restart",
                                 True, (200, 200, 200))
        self.screen.blit(msg1, msg1.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 40)))
        self.screen.blit(msg2, msg2.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 20)))

    def draw(self):
        """Render everything: background, asteroids, ship, HUD."""
        self.screen.fill(self.current_level["bg"])   # Paitning background 

        # Draw distant stars
        rng = random.Random(42) # A seed is used so that the stars ramain at the same position at eacht frame
        for _ in range(80):
            sx = rng.randint(0, SCREEN_W)
            sy = rng.randint(0, SCREEN_H)
            pygame.draw.circle(self.screen, (255, 255, 255), (sx, sy), 1)

        for ast in self.asteroids:
            ast.draw(self.screen)

        self.ship.draw(self.screen)
        self.draw_hud()             # Drawn last so it overlaps all other parts

        if self.game_over:
            self.draw_game_over()   # Overlaps everything

        pygame.display.flip()       # Show the new frame created (flip)

    # ------------------------------------------------------------------
    # Main entry-point
    # ------------------------------------------------------------------
    def run(self):
        """Start the game loop; runs until the player quits."""
        running = True
        while running:
            # dt capped at 0.05 s to prevent teleportation after lag spike
            dt = min(self.ticker.tick(FPS) / 1000.0, 0.05)
            running = self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
# Run the game if executed via the terminal.
if __name__ == "__main__":
    Game().run()


# In[ ]:





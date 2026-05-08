#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# For this game i used pygame to run it since its the most optimal for my case.
import pygame     
import math         
import random       
import sys

#These are the general gameplay constants which are very basic. In eah level the planet can survive up to 3 meteor crashes before it gets detroyed.

WIDTH, HEIGHT = 1000, 800   
FPS           = 60        
SHIP_SPEED   = 250   
BULLET_SPEED = 500   
PLANET_LIVES = 5     

#These are the colors of each item in the game defined as RGB tuples
BLACK  = (0,   0,   0)     
WHITE  = (255, 255, 255)   
YELLOW = (255, 220,  50)   
GRAY   = (160, 160, 160)   
GREEN  = (80,  220, 120)   
RED    = (220,  80,  80)   
BLUE   = (100, 160, 255)   
ORANGE = (255, 140,  50)  
CYAN   = (80,  220, 220)   
BROWN  = (160, 100,  50)   


# Here Ihave the game levels which are based on the real graviational attraction of the planets which is data obtained from NASA.
# Furthermore I have also added a count since the levels get harder there are more meteors per wave.
# The colors have also been names as RGB tuples throughout the game code for simplicity above.
LEVELS = [
    {"name": "Moon",    "gravity": 1.62, "speed": 16.2,  "count": 8,  "color": GRAY, "radius":17, "real_radius":1.736e6},
    {"name": "Mars",   "gravity": 3.72,  "speed": 37.2, "count": 6,  "color": RED, "radius":34,  "real_radius":3.389e6},
    {"name": "Earth", "gravity": 9.81, "speed": 98.1, "count": 4, "color": BLUE, "radius":63,  "real_radius":6.371e6}
]


class CelestialBody:
    """This is the basic class for every item in the game so they all share the same basic behaviour."""

    def __init__(self, x, y, radius, color):
        """Game Parameters:
        x, y   : float – position on screen presented in pixels
        radius : int   – size of the object on screen in pixels
        color  : tuple – RGB colour"""
        self.x      = float(x)  
        self.y      = float(y)     
        self.radius = radius      
        self.color  = color      

#This definition fills each cicle shown on screen by identifying the center of the circle by coordinates in integer form and then filling the color until the desired radius.
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, 
                           (int(self.x), int(self.y)),  # centre position
                           self.radius)           # radius of the circle
#I want to note I included integers cause pygame cant draw in decimals like 3.7 pixles of radius it has to be an integer.

# The following class is for the planets, so the objects being defended in all 3 levels. It is a subclass of all celestial bodies as it follows the same key behaviour.
class Planet(CelestialBody):
    """The planet is always fixed in the middle of the screen"""

    def __init__(self, color, radius, real_radius, gravity):
        super().__init__(WIDTH // 2, HEIGHT // 2,  # centre of the screen
                         radius=radius, color=color)
        self.lives = PLANET_LIVES                  # This line makes sure the planet starts with full lives which I set 3
        self.real_radius = real_radius
        self.gravity = gravity
    def hit(self):
        """ This is called when a meteor reaches the planet and it reduces lives by one and returns True if all lives are gone."""
        self.lives -= 1               # loses one life for every hit
        return self.lives <= 0        # If the lives go to zero the game ends. Game Over


class Spaceship(CelestialBody):
    """ The ship is controlled with the arrow keys and shoot with the spacebar"""

    def __init__(self):
        """Spawn the ship near the top of the screen, facing right."""
        super().__init__(WIDTH // 2, HEIGHT // 4,  # start near top centre
                         radius=13, color=CYAN)
        self.angle = 0.0   # Here the angle is zero meaning it starts pointing to the right of the screen, just above the planet.

    def update(self, keys, dt):
        vx, vy = 0.0, 0.0 # This line makes sure the ship starts at 0 velocty in both the x and y direction.
# These lines correspond to the arrow key movement where the max velocity is the ship speed set in the beggining.
        if keys[pygame.K_LEFT]:  vx = -SHIP_SPEED   # move left
        if keys[pygame.K_RIGHT]: vx =  SHIP_SPEED   # move right
        if keys[pygame.K_UP]:    vy = -SHIP_SPEED   # I want to note that I found out that this actually moves up due to the axes being inverted in pygame.
        if keys[pygame.K_DOWN]:  vy =  SHIP_SPEED   # SO this moves down
#!= means that it is not equal to so in this case when the ship is not stationary so moving in some direction it uses the arctan identity to convert the x and y direction of mtion in order for the ship to face in the same direction of motion.
        if vx != 0 or vy != 0:
            #I want to note that the angle is in radians
            self.angle = math.atan2(vy, vx)

#The self.x and self.y are the coordinates of the spaceship at a given instance and are designed so that they dont leave the screen by setting a maximu position.
# Also the vx*dt is the speed*time so the distance and makes sure that the ship travels at a constant speed regardless of fps of the game.
# The minimum takes either the width of the screen minus the radius of the ship or the distance it travelled, whichever is smaller.
        self.x = max(self.radius, min(WIDTH  - self.radius, self.x + vx * dt))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y + vy * dt))

    def shoot(self):
        """I created a bullet fired from the ship's nose in the direction the ship is currently facing."""
# Here i calculate teh position of the nose so that the bullet shoots from that point and not the centre of the ship.
        nx = self.x + math.cos(self.angle) * self.radius  
        ny = self.y + math.sin(self.angle) * self.radius
        
#Similar to the nose position, this shoots the bullet from the nose in both an x and y component. Bullet velocity: speed scaled by cos/sin of angle gives x and y components
        bvx = math.cos(self.angle) * BULLET_SPEED   # bullet x velocity
        bvy = math.sin(self.angle) * BULLET_SPEED   # bullet y velocity

        return Bullet(nx, ny, bvx, bvy)

    def draw(self, screen):
        """Draw the ship as a triangle pointing in the facing direction. The facing direction is the default spawn direction which is pointing at a radian angle of 0 so to the right."""
        # Calculate the 3 corner points of the triangle
        # angle+0 = tip, angle+2.4 = left wing, angle-2.4 = right wing
        pts = [(self.x + math.cos(self.angle + a) * self.radius,
                self.y + math.sin(self.angle + a) * self.radius)
               for a in (0, 2.4, -2.4)]          # A traingle is created where the radians of 2.4 are used to create an isosceles triangle.
        pygame.draw.polygon(screen, self.color, pts)


class Meteor(CelestialBody):
    """Spawns on a random screen edge and flies straight toward the planet."""
    def __init__(self, planet, speed):
        """
        Spawn at a random screen edge and aim at the planet.

        Parameters
        ----------
        planet : Planet – the target to fly toward
        speed  : float  – travel speed in pixels/second (based on level gravity)
        """
        # Here i pick a random edge of the screen for the meteors to spawn in 
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":      x, y = random.randint(0, WIDTH), 0        # top edge
        elif edge == "bottom": x, y = random.randint(0, WIDTH), HEIGHT   # bottom edge
        elif edge == "left":   x, y = 0, random.randint(0, HEIGHT)       # left edge
        else:                  x, y = WIDTH, random.randint(0, HEIGHT)   # right edge

        super().__init__(x, y, radius=13, color=BROWN)  # This is the creation of the meteor where its central coordinates and radius and color are defined.
        
        self.planet = planet
        self.vx = 0.0
        self.vy = 0.0

    def update(self, dt):
        """Move the meteor toward the planet each frame using real gravitational acceleration. It is asjusted by my set mupliplier otherwise the calculated meteor speed would be too slow."""
        dx = (self.planet.x - self.x)
        dy = (self.planet.y- self.y)
        dist = math.sqrt(dx*dx + dy*dy)
# Here I use the formula for gravitational acceleration use in astronomy however it is asjusted.
        acceleration = (self.planet.gravity * (self.planet.radius / dist)**2) * 700
        
        self.vx += (dx / dist) * acceleration * dt
        self.vy += (dy / dist) * acceleration * dt
        
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        
    def hits(self, other):
        """Check if this meteor is overlapping with another body it uses circle collision: overlap when distance is less than the sum of radii. """
        dx, dy = self.x - other.x, self.y - other.y         # These are distance components
        return math.sqrt(dx*dx + dy*dy) < self.radius + other.radius  # If this returns true it means their positions overlap so there is a collision between the meteor and the planet.

class Bullet(CelestialBody):
    """A bullet fired by the spaceship that travels in a straight line."""

    def __init__(self, x, y, vx, vy):
        """
        Parameters:
        x, y   : float – starting position
        vx, vy : float – velocity components in pixels per second
        """
        super().__init__(x, y, radius=4, color=YELLOW)  # The bullet is represented as a small yellow circle
        self.vx = vx   # horizontal speed - x direction
        self.vy = vy   # vertical speed - y - direction

    def update(self, dt):
        """Moves the bullet forward each frame. It updates its position in the window per frame."""
        self.x += self.vx * dt
        self.y += self.vy * dt 
# Here I call that if the bullet leaves the 4 screen boundaries then it disappears.
    def off_screen(self):
        """Return True if the bullet has travelled outside the visible screen."""
        return self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT


class Game:
    """This class covers everything in the game from the renderig to all object to the specific rules of the game."""

    def __init__(self):
        """Initialise pygame, create the window, and load the first level."""
        pygame.init()                                          # This starts the game
        self.screen  = pygame.display.set_mode((WIDTH, HEIGHT))  # Here the window is created which i defined in the very beggining with the pixel parameters.
        pygame.display.set_caption("Planet Defender")         # window title
        self.clock   = pygame.time.Clock()                    # Here I control the FPS of the game which I also defined in the first few lines
        self.font    = pygame.font.SysFont("monospace", 16)   # small font for HUD
        self.bigfont = pygame.font.SysFont("monospace", 28, bold=True)  # large font
        self.level_i = 0          # Here I start at the first level fo index 0 which is the moon.
        self.load_level()         # This sets up all the objects so it loads them in the level.

    def load_level(self):
        """Reset all game objects for the current level."""
        lv           = LEVELS[self.level_i]          # Here i get the levels from the Dictionary
        self.lv      = lv                         
        self.planet  = Planet(lv["color"], lv["radius"], lv["real_radius"], lv["gravity"])# Here the plaent is loaded with all the parameters.
        self.ship    = Spaceship()                   # When the level loads the ship is created in 
        self.meteors = [Meteor(self.planet, lv["speed"])
                        for _ in range(lv["count"])] # Count corresponds to the number of meteors per wave, where they only dissapear is the player shoots them or they reach the planet.
        self.bullets   = []        # empty list of bullets at start
        self.destroyed = 0         # count of meteors destroyed this level
        self.cooldown  = 0.0       # Starts at 0 cooldown so the player can start shooting instantly.
        self.phase     = "playing" # This is the game state which is in playing.

    def run(self):
        """Main game loop runs forever until the player destroys all asteroids or game over."""
        while True:
            dt = self.clock.tick(FPS) / 1000.0  # time since last frame in seconds
            self._events()   # This handles the keyboard input
            self._update(dt) # This updates the positions of all objects every frame
            self._draw()     # This draw and fills and colors all required objects on the screen

    def _events(self):
        """Process all pygame events this frame."""
        for e in pygame.event.get():
            if e.type == pygame.QUIT:              # player closed the window
                pygame.quit(); sys.exit()          # clean up and exit

            if e.type == pygame.KEYDOWN:
# for every event e in the game it loops them one by one, mainly the arrow and spacebar presses
                if (e.key == pygame.K_SPACE and
                        self.phase == "playing" and self.cooldown <= 0):
                    self.bullets.append(self.ship.shoot())  # This line states that if I pres the space bar and the game is still in the playing phase not the manu, it will shoot a bullet with a cooldown of 0.25 seconds.
                    self.cooldown = 0.25   # I allowed for a small cooldown of 0.25 since the last levels gets very challenging

# This line prevents accidental restarts by only letting you press the R key when you are going to the next level or game over screen.
                if e.key == pygame.K_r and self.phase != "playing":
                    if self.phase == "won":
# Here I advance to the next level and after you beat the game you can play again right from the start.
                        self.level_i = (self.level_i + 1) % len(LEVELS)
                    self.load_level()   # Here everything is reset to the beggining.

    def _update(self, dt):
        """Updating the positions over each frame and checking all collisions."""
        if self.phase != "playing":
            return   #Here the updates are skipped if Im in a win or lose condition or in other words im not curtrently playing.

        self.cooldown -= dt   #The time is negative to countdown the cooldown, not add time on top of it.

# This line updates the position of the ship based on the arrow input
        self.ship.update(pygame.key.get_pressed(), dt)

# Remove bullets that have left the screen
        self.bullets = [b for b in self.bullets if not b.off_screen()]

# Moves all bullets forwards by calling their method
        for b in self.bullets:
            b.update(dt)

# Moves each meteor and check if it has hit the planet
        for m in self.meteors[:]:   # Here i make a loop of the copy of the list of meteors so they can be removes if shot at.
            m.update(dt)
            if m.hits(self.planet):          
                self.meteors.remove(m)          
                if self.planet.hit():         
                    self.phase = "lost"; return 
# Keeps spawning meteors everywave and keeps the waves consistent.
                self.meteors.append(Meteor(self.planet, self.lv["speed"]))

        # Check each bullet against each meteor for a hit
        for b in self.bullets[:]:
            for m in self.meteors[:]:
                if m.hits(b):                   # If the bullet overlaps the position of the meteor they destroy each other leaving nothing left.
                    self.bullets.remove(b)       
                    self.meteors.remove(m)       
                    self.destroyed += 1      # Here i added this to make sure that one bullet can only kill one meteor.
                    break                   

# The win condition I set is that you have to destroy double the meyteor weave count to clear the level. If that happens you win the level.
        if self.destroyed >= self.lv["count"] * 2:
            self.phase = "won"
        elif len(self.meteors) == 0:
# If the game isnt over but all meteors are s=detsroyed a new random wave is deployed.
            self.meteors = [Meteor(self.planet, self.lv["speed"])
                            for _ in range(self.lv["count"])]

    def _draw(self):
        """Render all game objects and UI to the screen."""
        self.screen.fill(BLACK)          # clear screen with black background
        self.planet.draw(self.screen)    # draws the planet in the centre
        self.ship.draw(self.screen)      # draws the player's spaceship
        for b in self.bullets:
            b.draw(self.screen)          # draws each bullet
        for m in self.meteors:
            m.draw(self.screen)          # draws each meteor
        self._hud()                      # draws the heads-up display
        if self.phase != "playing":
            self._overlay()              # draws win/loss overlay if needed
        pygame.display.flip()            # pushes everything to the screen

    def _hud(self):
        """Draw the heads-up display showing level, gravity, player lives and progress."""
# The level name is displayed on the top left while drawing the relevant level title
        self.screen.blit(self.bigfont.render(
            f"Level {self.level_i+1}: {self.lv['name']} Level",
            True, WHITE), (20, 15))

# The gravity value is displayed toghether with the planet lives and the total meteors detroyed
        self.screen.blit(self.font.render(
            f"Real gravity: {self.lv['gravity']} m/s²  |  "
            f"Lives: {self.planet.lives}  |  "
            f"Meteors: {self.destroyed}/{self.lv['count']*2}",
            True, GRAY), (20, 52))

# This is a slightly darked transparent overlay at the win/loss screen
    def _overlay(self):
        ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # transparent surface filling the entire dimensions of the screen.
        ov.fill((0, 0, 0, 160))          # fill with semi-transparent black
        self.screen.blit(ov, (0, 0))     # draw it over the game

# Here I chose the message to the player based on the outcome.
        if self.phase == "won":
            t, c, s = f"WELL DONE PILOT!!! {self.lv['name'].upper()} DEFENDED!", GREEN, "Press R for next level"
        else:
            t, c, s = "OH NOOOOOOO, THE PLANET IS DESTROYED!", RED, "Press R to try again"
# Here i rendered the titles and subtitles for the win/loss screen.
        ts = self.bigfont.render(t, True, c)   # render title text
        ss = self.font.render(s,  True, WHITE) # render subtitle text

# Here i centered these texts in the middle of the screen

        self.screen.blit(ts, (WIDTH//2 - ts.get_width()//2, HEIGHT//2 - 30))
        self.screen.blit(ss, (WIDTH//2 - ss.get_width()//2, HEIGHT//2 + 15))

if __name__ == "__main__":
    Game().run()   # It creates the game and runs the game loop. The game only runs when you excecute the file directly.


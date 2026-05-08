#Astronomy themed bullet hell game
#Read through and make sure I understand all the code, and change + add comments where necessary
#!pip install arcade
#Imports for the game
import arcade
import random
import math
import arcade.gui

#Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "The Greatest PROGNUM Game Ever Created"
SPEED = 5
SCALING = 1.0

#Open m101.fits and get its data to use
from astropy.visualization import ZScaleInterval
from astropy.io import fits
from matplotlib import pyplot as plt

#Background image
#Remove axes, ticks, and whitespace when saving the image
data = fits.getdata("190515_Li_00000080.fits") 
zscale = ZScaleInterval() #Loads the image without needing to compute a full image histogram
fig, ax = plt.subplots(figsize=(SCREEN_WIDTH / 100, SCREEN_HEIGHT / 100), dpi=100)
ax.imshow(zscale(data), cmap="twilight")
ax.axis('off')  #Hide axes
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  #Remove border/margins
plt.savefig("bkg.png", bbox_inches='tight', pad_inches=0, dpi=100)
plt.close(fig)  #Close the figure to free resources

#Process "m101.fits" the same as the background, as an enemy sprite
m101_data = fits.getdata("m101.fits")
m101_zscale = ZScaleInterval()
fig2, ax2 = plt.subplots(figsize=(SCREEN_WIDTH / 100, SCREEN_HEIGHT / 100), dpi=10)
ax2.imshow(m101_zscale(m101_data), cmap="twilight")
ax2.axis('off')  #Hide axes
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove border/margins
plt.savefig("enemy.png", bbox_inches='tight', pad_inches=0, dpi=10)
plt.close(fig2)  #Close the figure to free resources

#Bullet hell enemy pattern
class BulletHellEnemy(arcade.Sprite):
    """An enemy in a bullet hell pattern, moves outward in a direction."""
    def __init__(self, image_file, x, y, angle_deg, speed):
        super().__init__(image_file, scale=1)
        self.center_x = x
        self.center_y = y
        self.angle_deg = angle_deg
        self.speed = speed

    def update(self, *args, **kwargs): #*args and *kwargs make it so that there is an unspecified amt of arguments 
        """Move in the direction specified by angle_deg at the designated speed."""
        radians = math.radians(self.angle_deg)
        dx = self.speed * math.cos(radians)
        dy = self.speed * math.sin(radians)
        self.center_x += dx
        self.center_y += dy

        #Remove if off screen
        if (self.center_x < -20 or self.center_x > SCREEN_WIDTH + 20 or #-20 so that enemies are fully offscreen before being deleted
            self.center_y < -20 or self.center_y > SCREEN_HEIGHT + 20):
            self.remove_from_sprite_lists()

#Game itself
class PROGNUMGAME(arcade.Window):

    """Bullet hell astronomy game

    Player can move anywhere but off screen

    Random number of enemies appear at a random position anywhere in a circular pattern

    Being hit ends the game

    """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.setup()

    def setup(self): #All initialization code separated to allow resetting the game easily
        #Create sprite lists
        self.all_sprites = arcade.SpriteList()
        self.projectiles_list = arcade.SpriteList()
        self.enemies_list = arcade.SpriteList()   #All bullet hell enemies

        self.game_over = False #Set game over flag to false
        self.enemies_killed = 0 #Set counter for enemies killed to 0

        #Create the player sprite
        character_width = 50
        character_height = 50
        self.player = arcade.Sprite(
            "chara.png",
            width=character_width, height=character_height,
            center_x=self.width // 2, center_y=100, angle=270 #Character's position
        )
        self.player.change_x = 0 #Speed set to 0
        self.player.change_y = 0
        self.all_sprites.append(self.player)

        #Input flags
        self.up = self.down = self.right = self.left = False

        #Background image (done like this to avoid some errors)
        self.bkg_sprite = arcade.SpriteList()
        self.background_sprite = arcade.Sprite("bkg.png")
        self.background_sprite.center_x = self.width // 2
        self.background_sprite.center_y = self.height // 2
        #Calculate the scaling factor so the background image fits the window
        width_scale = self.width / self.background_sprite.width
        height_scale = self.height / self.background_sprite.height
        self.background_sprite.scale = min(width_scale, height_scale) #Take the smaller of the scaling factors so the image doesnt change aspect ratio
        self.background_sprite.width = self.width
        self.background_sprite.height = self.height
        self.bkg_sprite.append(self.background_sprite)

        #Timer for bullet hell patterns
        self.bullet_hell_timer = 0
        self.bullet_hell_interval = 90   #Frames between bursts, change to make it easier/harder!

    def spawn_enemy_pattern(self):
        """Spawn a radial burst of bullet hell enemies from the top center."""
        num_enemies = random.randint(1, 15)  #Random number of enemies in the pattern
        speed = 3 
        start_x = random.randint(50, self.width - 50) #Spawns at a random point in the window
        start_y = random.randint(self.height//3, self.height - 50) #In the top 2/3rds so that player can stay at the bottom to kill enemies (fewer "bs" deaths, more skill based)
        for i in range(num_enemies):
            angle = i * 360 / num_enemies #Makes each enemy go a different direction
            enemy = BulletHellEnemy("enemy.png", start_x, start_y, angle, speed) 
            self.enemies_list.append(enemy)
            self.all_sprites.append(enemy)

    def on_draw(self):
        self.clear() #Clear the window (blank screen each frame)
        self.bkg_sprite.draw() 
        self.all_sprites.draw() #Creates all sprites
        
        #Draw number of enemies killed at the top left
        arcade.draw_text(
            f"Enemies Killed: {self.enemies_killed}",
            10, self.height - 30,
            arcade.color.WHITE, font_size=22,
            anchor_x="left", anchor_y="top"
        )
        
        if self.game_over:
            arcade.draw_lrbt_rectangle_filled(0, self.width, 0, self.height, arcade.color.BLACK) #Makes background black by creating a black rectangle
            arcade.draw_text(
                "GAME OVER",
                self.width // 2, self.height // 2 + 50,
                arcade.color.RED, font_size=56,
                anchor_x="center", anchor_y="center", bold=True, #Centers text relative to position, so we do not need to take it into account
            )
            arcade.draw_text(
                "Press ESC to quit",
                self.width // 2, self.height // 2 - 40,
                arcade.color.WHITE, font_size=26,
                anchor_x="center", anchor_y="center"
            )
            arcade.draw_text(
                "Press R to restart",
                self.width // 2, self.height // 2 - 80,
                arcade.color.WHITE, font_size=22,
                anchor_x="center", anchor_y="center"
            )

    def on_update(self, delta_time: float): #delta_time represents the time since last update; necessary
        if self.game_over:
            return

        #Updates the position of all game objects
        dx = dy = 0
        #Handles player direction 
        if self.up: dy += SPEED
        if self.down: dy -= SPEED
        if self.left: dx -= SPEED
        if self.right: dx += SPEED
        self.player.change_x = dx
        self.player.change_y = dy

        #Move all sprites (handled by arcade)
        self.all_sprites.update()

        #Stop the player going off screen
        min_x = self.player.width // 2 # // rounds result down to nearest whole number after dividing
        max_x = self.width - self.player.width // 2 #These functions obtain the edge of the player sprite
        min_y = self.player.height // 2
        max_y = self.height - self.player.height // 2
        self.player.center_x = max(min_x, min(self.player.center_x, max_x)) #Clamps player pos s.t. they cannot go past these boundaries
        self.player.center_y = max(min_y, min(self.player.center_y, max_y)) #Bcs of how arcade handles sprites (from the centre), we make the min the player can go be half the width of the sprite

        #Bullet hell pattern spawn (timer counts every update, i.e. every frame)
        self.bullet_hell_timer += 1
        if self.bullet_hell_timer >= self.bullet_hell_interval: #If timer = interval, spawn enemies and reset timer
            self.spawn_enemy_pattern()
            self.bullet_hell_timer = 0

        #Game over if player hits any enemy
        hit_enemies = arcade.check_for_collision_with_list(self.player, self.enemies_list)
        if hit_enemies:
            self.game_over = True

        #Projectiles kill bullet hell enemies
        for enemy in self.enemies_list[:]:
            projectiles_hit = arcade.check_for_collision_with_list(enemy, self.projectiles_list)
            if projectiles_hit:
                enemy.remove_from_sprite_lists()
                self.enemies_killed += 1 #Increase counter for every enemy killed
                for proj in projectiles_hit:
                    proj.remove_from_sprite_lists()
                    if proj in self.all_sprites:
                        self.all_sprites.remove(proj)

        #Projectiles update
        self.projectiles_list.update()
        #Remove projectile if off screen
        for projectile in self.projectiles_list[:]:
            if (projectile.center_y > self.height + 20 or projectile.center_y < -20 or
                projectile.center_x > self.width + 20 or projectile.center_x < -20):
                projectile.remove_from_sprite_lists()
                if projectile in self.all_sprites:
                    self.all_sprites.remove(projectile)

    def on_key_press(self, key: int, modifiers: int):
        if self.game_over:
            if key == arcade.key.ESCAPE:
                arcade.close_window() #Closes game w/ escape if game over
            elif key == arcade.key.R:
                self.setup() #Restarts if R
            return
        #WASD for movement
        if key == arcade.key.W:
            self.up = True
        elif key == arcade.key.S:
            self.down = True
        elif key == arcade.key.A:
            self.left = True
        elif key == arcade.key.D:
            self.right = True
        elif key == arcade.key.SPACE:
            #Shoot a projectile 
            projectile = arcade.Sprite("projectile.png", scale=0.09)
            projectile.center_x = self.player.center_x #Spawns at the centre of the player
            projectile.center_y = self.player.center_y
            projectile.change_y = 7 #Moves with speed 7
            self.projectiles_list.append(projectile)
            self.all_sprites.append(projectile)

    def on_key_release(self, key: int, modifiers: int):
        if self.game_over:
            return
        #Stops movement if movement key isnt being held
        if key == arcade.key.W:
            self.up = False
        elif key == arcade.key.S:
            self.down = False
        elif key == arcade.key.A:
            self.left = False
        elif key == arcade.key.D:
            self.right = False

if __name__ == "__main__": #Runs the game
    game = PROGNUMGAME()
    arcade.run()
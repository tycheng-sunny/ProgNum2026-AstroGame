#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pygame
import random
import math

class GameManager: # houses each function used by the game loop
    def __init__(self,screen,player_img,invader_imgs,bullet_img,font,game_over_font):
        self.screen=screen
        self.playerImage=player_img
        self.invaderImage=invader_imgs
        self.bulletImage=bullet_img
        self.font=font
        self.game_over_font=game_over_font
        # defines all functions within the class
        
    def show_score(self,x,y,score_val): # allows for updating of the score
        score=self.font.render("Points: "+str(score_val), True, (255, 255, 255))
        self.screen.blit(score,(x, y)) # str takesfunction input and returns as a string

    def game_over_display(self): # ends the loop when you die
        game_over_text=self.game_over_font.render("GAME OVER", True, (255, 255, 255))
        self.screen.blit(game_over_text,(200,250))

    def is_collision(self,x1,y1,x2,y2): # checks if the projectile collides with the ufo
        distance=math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))
        return distance<27

    def draw_player(self,x,y): # updates the posistion of the player
        self.screen.blit(self.playerImage,(x, y))

    def draw_invader(self,x,y,i): # updates the posistion of the ufo
        self.screen.blit(self.invaderImage[i],(x, y))

    def draw_bullet(self,x,y): # updates possistion of bullet
        self.screen.blit(self.bulletImage,(x+16,y+10))


pygame.init() # starts the game and defines the size of the screen
screen_width=800
screen_height=600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

score_val=0
font=pygame.font.Font('freesansbold.ttf', 20)
game_over_font=pygame.font.Font('freesansbold.ttf', 64)
background=pygame.image.load('space.png') # loads png files
B_width=background.get_width()
B_height=background.get_height()
B_shift=B_width*1.9,B_height*1.4
bg=pygame.transform.scale(background,B_shift) # expands png file to fit the background

original_Image = pygame.image.load('ship.png') # loads png file
p_width = original_Image.get_width()
p_height = original_Image.get_height()
shift=p_width*0.15,p_height*0.15
playerImage=pygame.transform.scale(original_Image, shift) # shrinks png to fit within collison box and make the game playable

# defines initial starting posistion and x-direction
player_X=370
player_Y=480
player_Xchange=0

# constructed as a list to allow for multiple to exist and be loaded by the class
invaderImage=[]
invader_X=[]
invader_Y=[]
invader_Xchange=[]
invader_Ychange=[]
N=8
    
for n in range(N): # randomally generates ufo in randoms points above a certain height with a set speed
    invader=pygame.image.load('ufo.png') # loads png file
    invader_X.append(random.randint(0, 735))
    invader_Y.append(random.randint(50, 150))
    invader_Xchange.append(2)
    invader_Ychange.append(40)
    I_width=invader.get_width()
    I_height=invader.get_height()
    I_shift=I_width*0.15,I_height*0.15
    invaderI=pygame.transform.scale(invader, I_shift) # shrinks png file to make the collision box obvious and hence game playable
    invaderImage.append(invaderI)

bullet=pygame.image.load('bullet.png') # loads png file
bullet_X=0 # initial posistions
bullet_Y=480
bullet_Ychange=10 # change in y direction
bullet_state="rest" # rest state = invisible/non-existance while fire state = visible/moving
b_width=invader.get_width()
b_height=invader.get_height()
b_shift=b_width*0.15,b_height*0.15
bulletImage=pygame.transform.scale(bullet, b_shift) # shrinks bullet to make the collision box obvious and hence the game playable

# defines the class for use within the code, hence allowing values to be pulled from it
game=GameManager(screen, playerImage, invaderImage, bulletImage, font, game_over_font)

# defines whether than game is running or not and if false displays a game over screen
running=True
is_game_over=False

while running: # game loop/contains code for class which is updated in real time
    screen.blit(bg, (0, 0)) # displays the background file
    for event in pygame.event.get():
        if event.type==pygame.QUIT: # stops the game if exited
            running=False

        if event.type == pygame.KEYDOWN: 
            if event.key==pygame.K_LEFT: # moves the player to the left when using left key
                player_Xchange=-5
            if event.key==pygame.K_RIGHT: # moves player to the right when using right key
                player_Xchange = 5
            if event.key==pygame.K_SPACE: # when pressing space if the bullet is in the rest state fires a bullet at the player posistion
                if bullet_state=="rest":
                    bullet_X=player_X
                    bullet_state="fire"

        # if event.type==pygame.KEYUP: causes the x-velocity to reset to zero when releasing a key
           #  if event.key==pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # player_Xchange=0

    if not is_game_over: # while the game is running limits the players movement to prevent moving off the screen
        player_X+=player_Xchange
        if player_X<=0: player_X = 0
        elif player_X>=736: player_X = 736

        # calculates for each invader
        for i in range(N):
            if invader_Y[i]>440: # causes a game over if the invader exceeds a certain point
                for j in range(N):
                   #  invader_Y[j]=2000 check if needed as invader disappears due to it
                    is_game_over=True
                break #  ends game loop due to game over

            # defines the change in the x and y direction for each indivdual invader
            invader_X[i]+=invader_Xchange[i]
            if invader_X[i]<=0:
                invader_Xchange[i]=2
                invader_Y[i]+=invader_Ychange[i]
            elif invader_X[i]>=736:
                invader_Xchange[i]=-2
                invader_Y[i]+=invader_Ychange[i]

            # detects whether or not the bullet collides with the invader
            collision=game.is_collision(invader_X[i], invader_Y[i], bullet_X, bullet_Y)
            if collision:
                bullet_Y=480 # resets posistion of the bullet when collision = true
                bullet_state="rest" #  resets state of bullet
                score_val+=1 
                invader_X[i]=random.randint(0, 735) # spawns a new invader when collision = true
                invader_Y[i]=random.randint(50, 150)

            game.draw_invader(invader_X[i],invader_Y[i],i) #  renders new invader

        if bullet_state=="fire":
            game.draw_bullet(bullet_X,bullet_Y)
            bullet_Y-=bullet_Ychange # controls vertical movement of the bullet
        
        if bullet_Y<=0: # if bullet goes off the screen resets state
            bullet_Y=480
            bullet_state="rest"

        game.draw_player(player_X,player_Y)
        game.show_score(10,10,score_val)
    else:
        game.game_over_display()
    pygame.display.update()


import turtle, random, math
import numpy as np 
#background is ngc6946

from player import Player
from badguy import Enemy
from bullet import Bullet
from score import Score

#screen
screen = turtle.Screen()
screen.setup(1000,600)
screen.bgcolor("blue")
screen.title("GET THEMMM")
screen.bgpic("background.png")
screen.tracer(0) #auto refresh off

pl = Player()
enemies = []
for i in range(9):
    enemies.append(Enemy())

b = Bullet()
s = Score()

# interaction between bullet and enemy

def bool_collision(a,b):
    distance = np.sqrt((a.xcor()-b.xcor())**2+(a.ycor()-b.ycor())**2)
    if distance <25:
        return True
    else:
        return False    

    
def shoot():
    if b.state == "Ready":
        b.state="Fire"

        x = pl.xcor()
        y = pl.ycor()+30
        b.goto(x,y)
        b.showturtle()

# user input stuff

screen.listen() #pay attention to the input
screen.onkey(pl.move_Left, "Left")
screen.onkey(pl.move_Right, "Right")
screen.onkey(shoot,"space") #spacebar fires

def end_game():
    
    for e in enemies:
        e.hideturtle()
    pl.hideturtle()
    b.hideturtle()

    s.goto(0,0)
    
    s.pd()
    s.write("HAH YOU LOST", align = "center", font = ("Comic Sans", 20))

#game loop
def game_loop():
    for enemy in enemies:
        x = enemy.xcor()
        x += enemy.speedamt #this moves the enemies horizontally
        enemy.setx(x) 

        if enemy.xcor()>425 or enemy.xcor()<-425:
            for e in enemies:
                e.sety(e.ycor()-25)
                #bounce back if it hits the wall AND lower it
            enemy.speedamt*=-1 #move enemy in other direction

        if b.state=="Fire" and bool_collision(b,enemy):
            b.hideturtle()
            b.state="Ready"
            b.goto(0,-400) #reset bullet and reset enemy below:
            enemy.setposition(random.randint(-300,300), random.randint(180,280))

            s.ScoreValue+=10
            s.clear()
            s.write(f"Score: {s.ScoreValue}", align="left", font=("Comic Sans",14))

        if bool_collision(pl,enemy): #if the enemy cillides with player:
            end_game()
            return
        
        if enemy.ycor()<=-200:
            end_game()
            return
        
    if b.state=="Fire":
        b.sety(b.ycor()+b.speedamt)

        if b.ycor()>300:
            b.hideturtle()
            b.state="Ready"
        
    screen.update()
    screen.ontimer(game_loop,20)

game_loop()
screen.mainloop()  # keeps the window open
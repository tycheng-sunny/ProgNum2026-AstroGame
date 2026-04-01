#Galaxy Finder
'''
High-score game: Catalogue each galaxy before they disappear!
'''

import turtle
import math
import random

galaxy_catalogue = {

}

# Screen Set-up
screen = turtle.Screen()
screen.bgcolor('black')
screen.title('Galaxy Finder')

#Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color('white')
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

#Create player
player = turtle.Turtle()
player.color('green')
player.shape('triangle')
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90)

playerspeed = 15

#Choose # of galaxies
number_of_galaxies = 5
#Create empty list of galaxies
galaxies = []

#Add galaxies to the list
for i in range(number_of_galaxies):
    #Create galaxy
    galaxies.append(turtle.Turtle())

for galaxy in galaxies:
    galaxy.color('blue')
    galaxy.shape('circle')
    galaxy.penup()
    galaxy.speed(0)
    x = random.randint(-200,200)
    y = random.randint(-200,-100)
    galaxy.setposition(x, y)

galaxyspeed = 2

#Create the beam
beam = turtle.Turtle()
beam.color('yellow')
beam.shape('square')
beam.penup()
beam.speed(0)
beam.shapesize(.3,.3)
beam.hideturtle()

beamspeed = 30

#Beam state
#ready - ready to shoot
#shoot - beam is being shot
beamstate = 'ready'

class Player:
    def __init__(self):
        ...

    #Player actions
    def move_left(self):
        x = player.xcor()
        x -= playerspeed
        if x < -280:   #Stops player from going off-screen
            x = -280
        player.setx(x)

    def move_right(self):
        x = player.xcor()
        x += playerspeed
        if x > 280:   #Same as before
            x = 280
        player.setx(x)

    def fire_beam(self):
        #Make beamstate a global if it needs changes
        global beamstate
        if beamstate == 'ready':
            beamstate = 'fire'
            #Move beam to just above the player
            x = player.xcor()
            y = player.ycor() + 10
            beam.setposition(x,y)
            beam.showturtle()

def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False

#Keyboard bindings
P = Player()
turtle.listen()
turtle.onkey(P.move_left, 'Left')
turtle.onkey(P.move_right, 'Right')
turtle.onkey(P.fire_beam, 'space')

#Main game loop
while True:

    for galaxy in galaxies:
        #Move the galaxies
        x = galaxy.xcor()
        x += galaxyspeed
        galaxy.setx(x)

        #Move galaxies back and up
        if galaxy.xcor() > 280:
            y = galaxy.ycor()
            y += 40
            galaxyspeed *= -1
            galaxy.sety(y)

        if galaxy.xcor() < -280:
            y = galaxy.ycor()
            y += 40
            galaxyspeed *= -1
            galaxy.sety(y)

        # Check for collision
        if isCollision(beam, galaxy):
            #Make beam come back
            beamspeed *= -1
            #Replace galaxy
            x = random.randint(-200,200)
            y = random.randint(-200,-100)
            galaxy.setposition(x, y)

        if galaxy.ycor() > 280:
            print('Game Over')
            break

    #Move beam
    if beamstate == 'fire':
        y = beam.ycor()
        y += beamspeed
        beam.sety(y)

    #Reset beam and catalogue galaxy
    if beam.ycor() < -280:
        beam.hideturtle()
        beamstate = 'ready'
        beam.setposition(0, -270)
        beamspeed *= -1

    #Check whether beam is in-bounds
    if beam.ycor() > 270:
        beam.hideturtle()
        beamstate = 'ready'
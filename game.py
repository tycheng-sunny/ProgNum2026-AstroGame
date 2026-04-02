# Galaxy Finder
'''
High-score game: Catalogue each galaxy before they disappear!
'''

import turtle
import math
import random
import time

galaxy_catalogue = [
    'Andromeda',
    'Messier 32', 'Messier 110',
    'NGC 147', 'NGC 185',
    'Andromeda Satellite Galaxies (And I–XXII)',
    'Milky Way',
    'Sagittarius Dwarf Galaxy', 'Large Magellanic Cloud',
    'Small Magellanic Cloud', 'Canis Major Dwarf Galaxy',
    'Ursa Minor Dwarf Galaxy', 'Draco Dwarf Galaxy',
    'Carina Dwarf Galaxy', 'Sexans Dwarf Galaxy',
    'Sculptor Dwarf Galaxy', 'Fornax Dwarf Galaxy',
    'Leo I & II', 'Ursa Major I & II Dwarf Galaxies'
]

player_catalogue = []

# Screen Set-up
screen = turtle.Screen()
screen.bgcolor('black')
screen.title('Galaxy Finder')
turtle.bgpic('m101.png')

# Draw border
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

# Score (will also act as 'difficulty')
score = 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color('white')
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = f'Score: {score}'
score_pen.write(scorestring, False, align='left', font=('Arial', 14, 'normal'))
score_pen.hideturtle()

# Galaxy catalogued message
score = 0
catalogue_pen = turtle.Turtle()
catalogue_pen.speed(0)
catalogue_pen.color('white')
catalogue_pen.penup()
catalogue_pen.setposition(150, 0)
catalogue_pen.hideturtle()

# Create player
player = turtle.Turtle()
player.color('green')
player.shape('triangle')
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90)

playerspeed = 15

# Choose # of galaxies
number_of_galaxies = 5
# Create empty list of galaxies
galaxies = []

# Add galaxies to the list
for i in range(number_of_galaxies):
    # Create galaxy
    galaxies.append(turtle.Turtle())

for galaxy in galaxies:
    galaxy.color('blue')
    galaxy.shape('circle')
    galaxy.penup()
    galaxy.speed(0)
    x = random.randint(-200,200)
    y = random.randint(-200,-100)
    galaxy.setposition(x, y)

galaxyspeed = 3 + 0.01 * score
position_offset = 0   # To be used later in making galaxies appear farther up

# Create the beam
beam = turtle.Turtle()
beam.color('yellow')
beam.shape('square')
beam.penup()
beam.speed(0)
beam.shapesize(.3,.3)
beam.hideturtle()

beamspeed = 30

# Beam state
# ready - ready to shoot
# shoot - beam is being shot
beamstate = 'ready'

class Player:
    def __init__(self):
        ...

    # Player actions
    def move_left(self):
        x = player.xcor()
        x -= playerspeed
        if x < -280:   # Stops player from going off-screen
            x = -280
        player.setx(x)

    def move_right(self):
        x = player.xcor()
        x += playerspeed
        if x > 280:   # Same as before
            x = 280
        player.setx(x)

    def fire_beam(self):
        # Make beamstate a global if it needs changes
        global beamstate
        if beamstate == 'ready':
            beamstate = 'fire'
            # Move beam to just above the player
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

# Keyboard bindings
P = Player()
turtle.listen()
turtle.onkey(P.move_left, 'Left')
turtle.onkey(P.move_right, 'Right')
turtle.onkey(P.fire_beam, 'space')

# Main game loop
while len(galaxy_catalogue) != 0:

    for galaxy in galaxies:
        # Move the galaxies
        x = galaxy.xcor()
        x += galaxyspeed
        galaxy.setx(x)

        # Move galaxies back and up
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
            # Make beam come back
            beamspeed *= -1
            # Replace galaxy
            x = random.randint(-200,200)
            y = random.randint(-200 + position_offset, -100 + position_offset)
            galaxy.setposition(x, y)
            position_offset = score if score < 350 else 350
            # Update score
            score += 10
            scorestring = f'Score: {score}'
            score_pen.clear()
            score_pen.write(scorestring, False, align='left', font=('Arial', 14, 'normal'))
            # Catalogue galaxy
            rand_galaxy = galaxy_catalogue[random.randint(0, len(galaxy_catalogue) - 1)]
            player_catalogue.append(galaxy_catalogue[random.randint(0,len(galaxy_catalogue)-1)])
            msg = 'New Galaxy Catalogued: \n'
            cataloguestring = rand_galaxy
            catalogue_pen.write(msg + cataloguestring, False, align='right', font=('Arial', 20, 'normal'))
            galaxy_catalogue.remove(rand_galaxy)

        if galaxy.ycor() > 280:
            catalogue_pen.clear()
            losestring = 'Game Over!'
            lose_pen = turtle.Turtle()
            lose_pen.speed(0)
            lose_pen.color('white')
            lose_pen.penup()
            lose_pen.setposition(-100, 0)
            lose_pen.write(losestring, False, align='left', font=('Arial', 50, 'normal'))
            lose_pen.hideturtle()
            time.sleep(3)
            break

    # Move beam
    if beamstate == 'fire':
        y = beam.ycor()
        y += beamspeed
        beam.sety(y)

    # Reset beam
    if beam.ycor() < -280:
        beam.hideturtle()
        beamstate = 'ready'
        beam.setposition(0, -270)
        beamspeed *= -1
        catalogue_pen.clear()

    # Check whether beam is in-bounds
    if beam.ycor() > 270:
        beam.hideturtle()
        beamstate = 'ready'

catalogue_pen.clear()
winstring = 'You Win!'
win_pen = turtle.Turtle()
win_pen.speed(0)
win_pen.color('white')
win_pen.penup()
win_pen.setposition(-100, 0)
win_pen.write(winstring, False, align='left', font=('Arial', 50, 'normal'))
win_pen.hideturtle()
time.sleep(3)
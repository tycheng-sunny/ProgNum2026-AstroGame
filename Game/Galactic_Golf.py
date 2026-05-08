import pygame
import pygame.gfxdraw
import pygame.mixer
import sys
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import time
import random

pygame.mixer.init()
pygame.mixer.music.load('music_alt.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()
print('===================')
print('Volume up for sound')
print('===================')

def rectmaker(num):
    dif  = 99999999999
    mynum = 0
    for i in range(num):
        b = num/(i+1)
        if (num%(i+1)==0) and abs(i+1-b)<dif:
            ar, br, dif = i+1, int(b), abs(i+1-b)
    return ar, br



def makemap(cond):
    data = fits.open(ogloc)[0].data
    fig, ax = plt.subplots()
    fig = plt.figure(frameon=False)
    fig.set_size_inches(4, 4)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    if len(np.shape(data)) > 2:
        data = np.mean(data, axis = 0)
    elif len(np.shape(data)) == 1:
        print(rectmaker(np.size(data)))
        data = np.reshape(data, rectmaker(np.size(data)))
    if cond:
        print(data)
    plt.imshow(data, cmap = 'inferno')
    fig.savefig('compmap.png', dpi=100)



TILE_COLOR = (255, 100, 98)
size = 10
SURFACE_COLOR = (167, 255, 100)
BALL_COLOR = (0, 0, 255)
ScreenWideness = 1000
ScreenHighness = 1000
ShootAngle = 0
FRICTION = 0.7
BUMPERS = 12
BUMPERSIZE = 70
POWER = 15
PAIN = False
setup = True
count = 0
run = True
firsttime = 0
upy, upx = np.random.rand()*ScreenHighness, np.random.rand()*ScreenWideness

sip = input('Enter filename (e.g. \'map.fits\'/\'m101.fits\'): ')
if sip != 'skip':
    print('Error: Try again')
    time.sleep(0.5)
    ogloc = input('Enter filename (e.g. \'map.fits\'/\'m101.fits\'): ')
    pee = int(input('Choose difficulty: 1, 2, or 3:  '))
    if pee > 3 :
        BUMPERS = 67
        print('==== Achievement: Good luck! ====')
    elif pee == 1:
        BUMPERS = 6
        FRICTION = 1
    elif pee == 2:
        print('Boring')
        time.sleep(1)
    elif pee == 3:
        BUMPERS = 20
        FRICTION = 0.3
        PAIN = True

    print('Connecting to Palantir servers...')
    time.sleep(3)
    print('Downloading \"Agartha-portalclientV7.ai\": |----------| ')
    time.sleep(0.9)
    print('Downloading \"Agartha-portalclientV7.ai\": |#---------| ')
    time.sleep(0.5)
    print('Downloading \"Agartha-portalclientV7.ai\": |##--------| ')
    time.sleep(0.9)
    print('Downloading \"Agartha-portalclientV7.ai\": |###-------| ')
    time.sleep(0.2)
    print('Downloading \"Agartha-portalclientV7.ai\": |####------| ')
    time.sleep(0.5)
    print('Downloading \"Agartha-portalclientV7.ai\": |#####-----| ')
    time.sleep(0.4)
    print('Downloading \"Agartha-portalclientV7.ai\": |######----| ')
    time.sleep(0.6)
    print('Downloading \"Agartha-portalclientV7.ai\": |#######---| ')
    time.sleep(0.5)
    print('Downloading \"Agartha-portalclientV7.ai\": |########--| ')
    time.sleep(0.1)
    print('Downloading \"Agartha-portalclientV7.ai\": |#########-| ')
    time.sleep(1)
    print('Downloading \"Agartha-portalclientV7.ai\": |##########| ')
    time.sleep(0.5)
    print('')
    print('Warning: ==== Lebronian infection detected ====')
    time.sleep(2)
    print('')
    print('Rendez-vous with BibiGPT at the core, and avoid contaminants at all cost.')
    time.sleep(5)
    print('Use the arrow keys to control Speed and Direction, Press the spacebar to shoot.')
    time.sleep(4)
else:
    print('==== Achievement: Dev mode, Activated! ====')
    ogloc = input('Enter filename: ')

if sip != 'skip':
    try:
        makemap(False)
    except:
        print('Bad file detected, please restart')
        time.sleep(2)
        sys.exit()
else:
    makemap(True)

pygame.init()
screen = pygame.display.set_mode((ScreenWideness, ScreenHighness))
imp = pygame.image.load("compmap.png")
bumpimg = pygame.image.load('lebon.png')
image = pygame.transform.scale(imp, (ScreenWideness, ScreenHighness))
bimage = pygame.transform.scale(bumpimg, (BUMPERSIZE, BUMPERSIZE))
mage = pygame.image.load('myto.png')
pimage = pygame.transform.scale(mage, (BUMPERSIZE, BUMPERSIZE))


class Bumper(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.Surface([size, size], pygame.SRCALPHA)
        image.blit(bimage, (x, y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.Surface([size, size], pygame.SRCALPHA)
        image.blit(pimage, (x,y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, highness, wideness):
        super().__init__()
        self.wideness = wideness
        self.highness = highness
        self.image = pygame.Surface([wideness, highness], pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (wideness//2, highness//2), wideness//2)
        self.rect = self.image.get_rect()

    def move(self, dx, dy, basevel):
        self.rect.x += dx*basevel
        self.rect.y += dy*basevel

data = fits.open(ogloc)[0].data
if len(np.shape(data)) > 2:
    data = np.mean(data, axis = 0)
elif len(np.shape(data)) == 1:
        print(rectmaker(np.size(data)))
        data = np.reshape(data, rectmaker(np.size(data)))
ys, xs = np.shape(data)
uf = 1/np.max(data)
sprite_list = pygame.sprite.Group()
bumperlist = []

myball = Ball(BALL_COLOR, size, size)
mypow = PowerUp(upx, upy, BUMPERSIZE)
myball.rect.x = 100
myball.rect.y = 100
sprite_list.add(myball)
sprite_list.add(mypow)

def centre():
    a = np.random.rand()*(ScreenHighness-BUMPERSIZE)
    while (a > (ScreenHighness/2)-BUMPERSIZE) and (a< (ScreenHighness/2)+BUMPERSIZE):
        a= np.random.rand()*(ScreenHighness-BUMPERSIZE)
    return a

def widd():
    a = np.random.rand()*(ScreenWideness-BUMPERSIZE)
    while (a > 100 - BUMPERSIZE) and (a< 100+BUMPERSIZE):
        a= np.random.rand()*(ScreenWideness-BUMPERSIZE)
    return a

bumps = [Bumper(widd(), centre(), BUMPERSIZE) for i in range(BUMPERS)]
bumps.append(Bumper(300, 600, BUMPERSIZE))
for i in bumps:
    sprite_list.add(i)

klok = pygame.time.Clock()
power = 0
pygame.display.set_caption("Galactic Golf DX")

screen.blit(image, (0, 0))
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()

    screen.blit(image, (0, 0))

    if (myball.rect.x > 990) or (myball.rect.x < 10) or (myball.rect.y > 990) or (myball.rect.y < 10):
        print('Out of bounds!')
        sys.exit()

    if firsttime < 5:
        for i in bumps:
            if i.rect.colliderect(myball.rect) or i.rect.collidepoint(int(ScreenWideness/2), int(ScreenHighness/2)):
                sprite_list.remove(i)
        sprite_list.update()

    if mypow.rect.colliderect(myball.rect):
        count -= 5
        time.sleep(3)
        basevel = 10
        ShootAngle = ShootAngle - 3.14159265358
        setup = False
    if firsttime > 5:
        for thing in bumps:
            if thing.rect.colliderect(myball.rect):
                print('you lose')
                if PAIN:
                    pygame.mixer.music.load('music.mp3')
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play()
                    time.sleep(5)
                sys.exit()


    if (abs(myball.rect.x - ScreenWideness/2) < 10) and abs(myball.rect.y - ScreenHighness/2) < 10:
        pygame.quit()
        print('You\'re winner')
        print(f'You took {count} shots!')
        if count == 67:
            print('=== Achievement: Tuff ahh Diddyblud ===')
        sys.exit()
    if setup:
        if keys[pygame.K_SPACE]:
            setup = False
        if keys[pygame.K_UP]:
            power += POWER
        if keys[pygame.K_DOWN]:
            power -= POWER
        if keys[pygame.K_RIGHT]:
            ShootAngle += 0.1
        if keys[pygame.K_LEFT]:
            ShootAngle -= 0.1
        xloc = myball.rect.x + 0.5*power*np.cos(ShootAngle)
        yloc = myball.rect.y + 0.5*power*np.sin(ShootAngle)
        pygame.gfxdraw.line(screen, int(myball.rect.x), int(myball.rect.y), int(xloc), int(yloc), (255, 0, 0))
        basevel = power/20
    else:
        if basevel > 0:
            myball.move(np.cos(ShootAngle), np.sin(ShootAngle), basevel)
            data_y = int((myball.rect.y/ScreenHighness)*ys)
            data_x = int((myball.rect.x/ScreenWideness)*xs)
            basevel = basevel - FRICTION*(data[data_x, data_y]/np.nanmax(data))
        elif basevel < 0:
            basevel = 0
            setup = True
            count += 1
        else:
            setup = True
            count += 1
    sprite_list.update()
    sprite_list.draw(screen)
    pygame.draw.circle(screen, (255, 255, 255), (ScreenWideness//2, ScreenHighness//2), 10)
    pygame.display.update()
    firsttime += 1


    klok.tick(60)

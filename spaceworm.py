import tkinter, random

#DATABASE
import pandas as pd

df = pd.read_csv("hygdata_v42.csv.gz")

df = df[df['proper'].notna()]
df = df[df['spect'].notna()]
columns_to_keep = ['proper', 'dist', 'mag', 'absmag', 'spect', 'lum']
stars_df = df[columns_to_keep]
stars_df = stars_df.sort_values(by='mag')
stars_df = stars_df[:50]

def star_info(number):
    """Generates information about current star for death screen"""
    chosen = stars_df.iloc[number]
    name = chosen['proper']
    distance = f"{chosen['dist']:.2f}"
    mag = f"{chosen['mag']:.2f}"
    absmag = f"{chosen['absmag']:.2f}"
    lum = f"{chosen['lum']:.2f}"
    color = chosen['spect'][0]
    
    #CREATES THE STAR INFO TEXT BOX
    c.create_rectangle(
        canvas/9,15*canvas/32,8*canvas/9,27*canvas/32,
        fill='ghostwhite', outline='white')
    c.create_text(
        canvas/2,13*canvas/24,
        text = 'CURRENT STAR:   ' + name, font = ('Small Fonts',int(canvas/30),'bold'))
    c.create_text(
        canvas/2,5*canvas/8,
        text = 'DISTANCE:   ' + distance + ' pc', font = ('Small Fonts',int(canvas/40)))
    c.create_text(
        canvas/2,2*canvas/3,
        text = 'MAGNITUDE:   ' + mag, font = ('Small Fonts',int(canvas/40)))
    c.create_text(
        canvas/2,17*canvas/24,
        text = 'ABSOLUTE MAGNITUDE:   ' + absmag, font = ('Small Fonts',int(canvas/40)))
    c.create_text(
        canvas/2,3*canvas/4,
        text = 'LUMINOSITY:   ' + lum + ' L☉', font = ('Small Fonts',int(canvas/40)))
    c.create_text(
        canvas/2,19*canvas/24,
        text = 'SPECTRAL TYPE:   ' + color, font = ('Small Fonts',int(canvas/40)))
    
def star_color(number):
    """Updates star color based on current star from database"""
    chosen = stars_df.iloc[number]
    color = chosen['spect'][0]
    colors = {
        'O': 'deepskyblue',
        'B': 'lightskyblue',
        'A': 'ghostwhite',
        'F': 'lightyellow',
        'G': 'gold',
        'K': 'orange',
        'R': 'red'
    }
    return colors.get(color,'ghostwhite')

#SIZE SETTINGS, CUSTOMIZABLE
grid = 20
square = 30
canvas = grid*square

main = tkinter.Tk()
c = tkinter.Canvas(
    width = canvas, height = square*(grid+2),
    bg = 'midnightblue')

#CREATE BACKGROUND CANVAS
def setup():
    global x, y, move, spots0, spots1, counter, f, choice
    c.create_rectangle(
        0,canvas,canvas,square*(grid+2),
        fill='ghostwhite', outline='white')
    for i in range(1000):
        x = random.randint(0,canvas)
        y = random.randint(0,canvas)
        c.create_rectangle(
            x,y,x+1,y+1,
            fill='ghostwhite', outline='ghostwhite')
    c.pack()
    
    #INITIAL CONDITIONS
    x = 0
    y = 0
    move = [1, 0]
    spots0 = []
    spots1 = []
    choice = random.randint(0, 49)
    
    counter = 0
    f = 0
    
    #CREATES FIRST STAR POSITION AND WORM HEAD
    star()
    c.create_rectangle(
        x*square,y*square,x*square+square,y*square+square,
        **worm_design)
    

def restart():
    """Restarts game settings for a new game"""
    c.delete('all')
    
    setup()
    game()

#MOVEMENT FUNCTIONS BINDED TO KEYBOARD ARROWS
def left(pos):
    global move
    if move != [1,0]:
        move = [-1,0]
def right(pos):
    global move
    if move != [-1,0]:
        move = [1,0]
def up(pos):
    global move
    if move != [0,1]:
        move = [0,-1]
def down(pos):
    global move
    if move != [0,-1]:
        move = [0,1]
        
c.bind_all('<Left>',left)
c.bind_all('<Right>',right)
c.bind_all('<Up>',up)
c.bind_all('<Down>',down)

def star():
    """Generates star location, making sure it's not in the worm"""
    global starx, stary
    while True:
        starx = random.randint(0, grid-1)
        stary = random.randint(0, grid-1)
        if [starx, stary] not in spots0:
            break

worm_design = {
    'fill': 'lime',
    'outline': 'white',
    'tags': 'delete'
}

def game():
    """Runs game"""
    global x, y, spots0, spots1, counter, f, starx, stary, choice
    
    #STOPS GAME
    if f == 1:
        return
    
    #RESTARTS GRAPHICS FOR NEW UPDATES
    c.delete('delete')
    
    #DEATH FUNCTION
    def death():
        """Draws death screen"""
        c.create_rectangle(
            canvas/4,canvas/8,3*canvas/4,canvas/2,
            fill='midnightblue', outline='midnightblue')
        c.create_text(
            canvas/2,canvas/4,
            text = 'You died!', font = ('Small Fonts',int(canvas/6),'bold'), fill='powderblue')
        score = 'score: ' + str(counter)
        c.create_text(
            canvas/2,canvas/4+int(canvas/7),
            text = score, font = ('Small Fonts',int(canvas/15),'bold'), fill='powderblue')
        star_info(choice)
        
        #RESTART BUTTON
        restart_button = tkinter.Button(
            main,
            text='RESTART',
            command=restart,
            font=('Small Fonts', 20, 'bold'),
            bg = 'ghostwhite',
            activebackground = 'lime')
        c.create_window(
            canvas/2, 9*canvas/10,
            window=restart_button, tag='delete')
    
    #EATING AND CREATING NEW STAR
    if x == starx and y == stary:
        star()
        counter += 1
        spots1 += [[]]
        choice = random.randint(1,49)
    
    star_design = {
        'fill': star_color(choice),
        'outline': 'white',
        'tags': 'delete',
}
        
    #DRAWS CURRENT STAR
    c.create_rectangle(
        starx*square,stary*square,square*(starx+1),square*(stary+1),
        **star_design)
    
    #MOVEMENT
    x = int(move[0])+x
    y = int(move[1])+y
    
    #DEATH BY HITTING YOURSELF
    if [x,y] in spots0:
        f = 1
        death()
    
    #ADDING TO WORM
    c.create_rectangle(
        x*square,y*square,x*square+square,y*square+square,
        **worm_design)   #DRAWS HEAD
    if counter > 0:   #IF WORM BODY IS LONGER THAN JUST HEAD
        for i in range(counter):
            c.create_rectangle(
                spots0[i][0]*square,spots0[i][1]*square,square*(spots0[i][0]+1),square*(spots0[i][1]+1),
                **worm_design)   #DRAWS BODY SQUARES IN PREVIOUS SPOTS
            spots1[i+1] = spots0[i]   #UPDATES LIST OF SPOTS OCCUPIED BY CURRENT WORM
        spots1[0] = [x,y]   #ADDS CURRENT HEAD SPOT
    else:
        spots1 = [[x,y]]   #ADDS HEAD SPOT
        
    #SCORE TEXT
    stars = 'STARS EATEN - ' + str(counter)
    c.create_text(
        canvas/2,canvas+square,
        text = stars, font = ('Small Fonts',25,'bold'),tags='delete')
    
    #DEATH BY HITTING WALLS
    if x>grid-1 or y>grid-1 or x<0 or y<0:
        f = 1
        death()
    
    #WORM BODY UPDATE
    spots0 = []
    for i in range(len(spots1)):
        spots0 += [spots1[i]]   #UPDATE AFTER MOVEMENT THIS LOOP, USED IN NEXT LOOP TO MOVE WORM ALONG THE SAME SPOTS
        
    c.after(100, game)

#START BUTTON
start_button = tkinter.Button(
    main,
    text='START',
    command=game,
    font=('Small Fonts', 20, 'bold'),
    bg = 'ghostwhite',
    activebackground = 'lime')
c.create_window(
    canvas/2, canvas/2,
    window=start_button, tag='delete')

setup()
#THIS FUNCTION SETS UP GAME, START BUTTON CALLS GAME FUNCTION. WHEN DEATH OCCURS, RESTART FUNCTION IS CALLED, WHICH DELETES
#EVERYTHING AND CALLS BOTH SETUP AND GAME AGAIN
    
main.mainloop()
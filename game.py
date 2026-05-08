from matplotlib.pyplot import figure, show, savefig, ioff, close, get_current_fig_manager
from astropy.io import fits
import matplotlib.image as mpimg
import numpy as np

ioff()

image=[]
image0=[]
back=[]
indexes=[0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7]
indexes=np.random.permutation(indexes)
for i in range(1,17):
    im=mpimg.imread(f'back{i}.png')
    back.append(im)

for i in range(1,9):
    im=mpimg.imread(f'image{i}.png')
    image0.append(im)

for i in indexes:
    image.append(image0[i])

imlist=back.copy()
flips=False
won=False
flipno=0
close=False

while not won:
    fig=figure(figsize=(5,5))
    manager = get_current_fig_manager()
    manager.window.wm_geometry("+50+50")
    for i in range(16):
        frame=fig.add_subplot(4,4,i+1)
        frame.imshow(imlist[i])
        frame.axes.xaxis.set_ticklabels([])
        frame.axes.yaxis.set_ticklabels([])
        frame.axes.xaxis.set_ticks([])
        frame.axes.yaxis.set_ticks([])
    show(block=False)
    if close==True:
        imlist[flip1]=back[flip1]
        imlist[guess]=back[guess]
        flipno-=2
        close=False
    try:
        guess=int(input("Enter the number of the card you want to flip: "))
        guess-=1
    except:
        print("Enter an integer")
        
    try:
        imlist[guess]=image[guess]
    except:
        print("Enter a valid integer")
    flipno+=1 
    if flips==False:
        flip1=guess
        flips=True
    else:
        flips=False
        if indexes[guess]!=indexes[flip1]:
            close=True
        if flipno==16:
            won=True
            print('You won!')
    
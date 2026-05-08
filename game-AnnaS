from astropy.io import fits
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np 

hdulist = fits.open('~/PROGNUM-repo/Task6/m101(1).fits')
dat = hdulist[0].data
datarr = np.asarray(dat, dtype='float64')

fig, axes = plt.subplots(2, 2, gridspec_kw={'wspace': 0, 'hspace': 0}, figsize=(5,5))

tl = (dat[265:530, 0:265])
tr = (dat[265:530, 265:530])
bl = (dat[0:265, 0:265])
br = (dat[0:265, 265:530])

axes[0, 0].axis('off')
axes[0, 1].axis('off')
axes[1, 0].axis('off')
axes[1, 1].axis('off')

print(f"Play a puzzle game. Guess where to put the four pieces. Choose top left, top right, bottom left, or bottom right")

part1 = input("Where to put the first piece?").strip().lower()
if part1 == 'top left':
    axes[0, 0].imshow(tl, origin='lower')
elif part1 == 'top right':
    axes[0, 1].imshow(tl, origin='lower')
elif part1 == 'bottom left':
    axes[1, 0].imshow(tl, origin='lower')
elif part1 == 'bottom right':
    axes[1, 1].imshow(tl, origin='lower')
else:
    print(f"Invalid position")
    sys.exit()

part2 = input("Where to put the second piece?").strip().lower()
if part2 == 'top left':
    axes[0, 0].imshow(tr, origin='lower')
elif part2 == 'top right':
    axes[0, 1].imshow(tr, origin='lower')
elif part2 == 'bottom left':
    axes[1, 0].imshow(tr, origin='lower')
elif part2 == 'bottom right':
    axes[1, 1].imshow(tr, origin='lower')
else: 
    print(f"Invalid position")
    sys.exit()

part3 = input("Where to put the third piece?").strip().lower()
if part3 == 'top left':
    axes[0, 0].imshow(bl, origin='lower')
elif part3 == 'top right':
    axes[0, 1].imshow(bl, origin='lower')
elif part3 == 'bottom left':
    axes[1, 0].imshow(bl, origin='lower')
elif part3 == 'bottom right':
    axes[1, 1].imshow(bl, origin='lower')
else: 
    print(f"Invalid position")
    sys.exit()

part4 = input("Where to put the fourth piece?").strip().lower()
if part4 == 'top left':
    axes[0, 0].imshow(br, origin='lower')
elif part4 == 'top right':
    axes[0, 1].imshow(br, origin='lower')
elif part4 == 'bottom left':
    axes[1, 0].imshow(br, origin='lower')
elif part4 == 'bottom right':
    axes[1, 1].imshow(br, origin='lower')
else: 
    print(f"Invalid position")
    sys.exit()

plt.show()

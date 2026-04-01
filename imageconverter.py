from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import zoom


hdul = fits.open("ngc6946.fits")
data = hdul[0].data
sliced = data[:,50,:]
hdul.close()
sliced = np.nan_to_num(sliced)


size = (600,1000)
zoom_factors = (size[0]/sliced.shape[0],size[1]/sliced.shape[1])
datanew = zoom(sliced,zoom_factors)
plt.imsave("background.png",datanew,cmap="plasma")

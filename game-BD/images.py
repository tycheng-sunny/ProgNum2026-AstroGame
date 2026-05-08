from astropy import coordinates as coords
from astroquery.sdss import SDSS
from matplotlib.pyplot import figure, show, savefig, ioff, close
from astropy.visualization import ImageNormalize, SinhStretch, AsymmetricPercentileInterval, LinearStretch,\
                                  LogStretch, PowerStretch, SqrtStretch, SquaredStretch,\
                                  HistEqStretch, ZScaleInterval
import numpy as np

ioff()

ra  = [160.9903, 167.8793, 179.3998, 148.9688, 34.6886, 169.732, 202.4696, 148.8882]
dec = [11.7038, 55.6742, 53.3747, 69.6797, -6.6390, 13.092, 47.1952, 69.0653]

class cards:

    def __init__(self,n):
        self.n=n

    def imdisplay(self, data,
                  ax,
                  vmin=None, vmax=None,
                  percentlow=1, percenthigh=99,
                  zscale=False,
                  scale='linear',
                  power=1.5,
                  cmap='gray',
                  **kwargs):
    
        if zscale:
            interval = ZScaleInterval()
            vmin, vmax = interval.get_limits(data)
        if vmin is None or vmax is None:
            interval = AsymmetricPercentileInterval(percentlow, percenthigh)
            vmin2, vmax2 = interval.get_limits(data)
            if vmin is None:
                vmin = vmin2
            if vmax is None:
                vmax = vmax2
    
        if scale == 'linear':
            stretch = LinearStretch(slope=0.5, intercept=0.5)
        if scale == 'sinh':
            stretch = SinhStretch()
        if scale == 'log':
            stretch = LogStretch()
        if scale == 'power':
            stretch = PowerStretch(power)
        if scale == 'sqrt':
            stretch = SqrtStretch()
        if scale == 'squared':
            stretch = SquaredStretch()
        if scale == 'hist':
            stretch = HistEqStretch(data)
            vmin = data.min(); vmax = data.max()
    
        norm = ImageNormalize(vmin=vmin, vmax=vmax, stretch=stretch)
        return ax.imshow(data, interpolation='none', origin='lower', norm=norm, cmap=cmap, **kwargs)

    def backs(self):
        for i in range(1,2*self.n+1):
            fig=figure()
            frame=fig.add_subplot(1,1,1)
            frame.plot([0,1],[0,1],color='gray')
            frame.set_facecolor('gray')
            frame.axes.xaxis.set_ticklabels([])
            frame.axes.yaxis.set_ticklabels([])
            frame.axes.xaxis.set_ticks([])
            frame.axes.yaxis.set_ticks([])
            frame.text(0.5, 0.5, f"{i}", horizontalalignment='center', verticalalignment='center', color='k', size=28)
            savefig(f'back{i}.png')
            close(fig)
        return None

    def images(self):
        for i in range(1,self.n+1):
            pos = coords.SkyCoord(ra[i-1], dec[i-1], unit="deg", frame="icrs")
            xid = SDSS.query_region(pos, radius='5 arcsec')
            hdulist = SDSS.get_images(matches=xid)
            hdu = hdulist[0]
            data = hdu[0].data
            fig=figure()
            frame=fig.add_subplot(1,1,1)
            self.imdisplay(data,frame, scale='power',cmap='rainbow')
            frame.axes.xaxis.set_ticklabels([])
            frame.axes.yaxis.set_ticklabels([])
            frame.axes.xaxis.set_ticks([])
            frame.axes.yaxis.set_ticks([])
            savefig(f'image{i}.png')
            close(fig)
        return None
        
cards=cards(8)
cards.images()
cards.backs()
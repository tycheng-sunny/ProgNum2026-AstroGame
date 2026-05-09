from astropy.coordinates import SkyCoord,AltAz,EarthLocation
from datetime import datetime,timedelta
from astropy.time import Time
from astropy import units as u


Groningen = EarthLocation(lat = '53.2192', lon='6.56667',height=7*u.m)

def LST(time=datetime.now()):
    """Local sidereal time for time input"""
    t = Time(time,location=Groningen,scale='utc')

    return t.sidereal_time('mean').deg


def EQ1_AZ(HA,DEC,time):
    """Converts first equatorial coordinates to azimuthal for a given time"""

    aa = AltAz(location=Groningen,obstime=Time(time))
    coord = SkyCoord(LST(time)-HA,DEC,unit='deg',frame='icrs')

    return (coord.transform_to(aa).az.deg,coord.transform_to(aa).alt.deg)


def AZ_EQ1(AZ,ALT,time,timezone=2):
    """Converts azimuthal coordinates to first equatorial for a given time"""
    if abs(ALT) > 90: # If the altitude goes above zenith or below nadir
        coord = SkyCoord(az=AZ,alt=90-ALT%90,unit='deg',frame='altaz',location=Groningen,obstime=Time(time))
    else:
        coord = SkyCoord(az=AZ,alt=ALT,unit='deg',frame='altaz',location=Groningen,obstime=Time(time))

    return (coord.transform_to('icrs').ra.deg,coord.transform_to('icrs').dec.deg)


def EQ1_EQ2(HA,time):
    """Converts hour angle to right ascension"""
    return LST(time)-HA


def EQ2_EQ1(RA,time):
    """Converts right ascension to hour angle"""
    return LST(time)-RA
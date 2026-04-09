########### MODULE IMPORTS (SELF DEVELOPED and global ones) ##################

from tkinter import *
from astroquery.skyview import SkyView
from astropy.coordinates import SkyCoord, AltAz
from astropy import units as u

import numpy as np

from displays import *
from controls import *
from output import *
from infobar import *
from converters2 import *

from datetime import datetime
from time import sleep


Groningen = EarthLocation(lat = '53.2192', lon='6.56667',height=7*u.m)

T0 = datetime.now() - timedelta(hours=2) # correction for timedelay, idk, why but sadly this is the case
Local_Sid_Time = LST(T0)

####################################################################



################### INTERFACE SETUP ###################

Height = 800
Width = 800

window = Tk()
window.geometry(f"{Width}x{Height}")
window.title('Observational simulation - version 1.3')

######### GLOBAL VARIABLES ######
timescale = 1  # Timescale in  !!e-2!! seconds
is_Standby = True
timer = 0

Azimuth = 0; Altitude = 0  # TELESCOPE STARTS AT (0,0)

Recta,Decl = AZ_EQ1(Azimuth,Altitude,T0)
HourAngle = EQ2_EQ1(Recta,T0)
##################################

top_section = DSP_Panels(window,starting_position=(Azimuth,Altitude)) # adds the 
op = Output(window)
navigators = ControlPanel(window,LST=Local_Sid_Time,azimuth=Azimuth,alt=Altitude)
b = InfoBar(window,T0)

########################################################



################ TASKS OF THE TELESCOPE ####################
def follow(RA,DEC,time,obs=False,remaining=0):
    """ 'Moves' the telescope and keeps it on the input target """

    global Azimuth # the variables of the telescope
    global Altitude
    global HourAngle

    ha = EQ2_EQ1(RA,time)  # calculates hour angle

    az,alt = EQ1_AZ(ha,DEC,time) # altaz corrds
    
    top_section.display(az,alt) # moves the arrows to the corresponding altaz positions
    navigators.update_all(az,alt,ha,RA,DEC) # updates the displayed coordinates

    b.refresh(T0,obs=obs,timer=remaining) # refreshes infobar time (and remaining observational tme if relevant)

    Azimuth = az
    Altitude = alt
    HourAngle = ha


def GoToTarget(RA,DEC,t_RA,t_DEC,time=T0): # steps (int): amount of steps taken from current to target, default 100
    """ Moves the telecope to the new target, while !pausing the time!"""

    global is_Standby  # defines global variables
    global Recta       # defines global variables
    global Decl        # defines global variables

    ha = EQ2_EQ1(RA,time)  # calculates hour angle
    t_ha = EQ2_EQ1(t_RA,time)  # calculates target hour angle

    az,alt = EQ1_AZ(ha,DEC,time) # default altaz corrds
    t_az,t_alt = EQ1_AZ(t_ha,t_DEC,time) # target altaz corrds

    steps = 100

    dAZ = -(t_az-az)/steps if (t_az-az) <= 180 else (t_az-az)/steps
    dALT = (t_alt-alt)/steps


    b.change_mode('Change target')
    op.clear_output()
    is_Standby = False

    for i in range(steps):

        az += dAZ
        alt += dALT

        if alt < 0:
            alt = 0

        top_section.rotate(angle=dAZ,current=(az,alt),axis=0)  # rotates starmap left/right
        top_section.rotate(angle=dALT,current=(az,alt),axis=1) # rotates starmap up/down

        ha,dec = AZ_EQ1(az,alt,time)
        ra = EQ1_EQ2(ha,time)

        top_section.display(az,alt) # moves the arrows to the corresponding altaz positions
        navigators.update_all(az,alt,ra,ha,dec) # updates the displayed coordinates (ha and ra scwitched here because for some reason the converter gives the opposite results)

        window.update()

    b.change_mode('Standby')
    is_Standby = True

    Recta = t_RA
    Decl = t_DEC


def Observation(RA,DEC,radius=1):
    """ One round of observation: returnes image from the selected coords """

    global is_Standby
    global T0

    is_Standby = False

    timer = 0

    b.change_mode('Observing')
    op.clear_output()
    op.bg.itemconfig(op.info,text="Observation in progress")

    Tstart = T0

    while (T0-Tstart).seconds < 10:

        T0 += timedelta(seconds=timescale/10)

        follow(RA,DEC,T0,obs=True,remaining=(T0-Tstart).seconds)

    b.change_mode('Downloading \nimage data')
    b.refresh(T0,obs=False)

    pos = SkyCoord(RA, DEC, unit="deg", frame="icrs")
    paths = SkyView.get_images(position=pos, survey='DSS', radius=radius*u.deg)

    try:
        op.add_output(paths[0][0].data)

    except: # if there is no data from the observation point
        op.bg.itemconfig(op.info,text="Observation was unsuccesful \n target change recommended")

    b.change_mode('Standby')

    is_Standby = True
############################################################


###################### TASK TRIGGERS #####################
def get_target():
    """ Gets the target coordinates from the entrys"""

    try:
        r = float(navigators.RA_input.get().replace(',','.').replace(' ','')) # avoiding misspelled right ascensions
        target_RA = r%360
        
    except: # if input is not a number
        navigators.canvas.itemconfig(navigators.valid_input,text='Invalid input')
        window.update()

        return
    
    try:
        d = float(navigators.DEC_input.get().replace(',','.').replace(' ','')) # avoiding misspelled declinations
        target_DEC = d%90 if d > 0 else d%-90

    except: # if input is not a number
        navigators.canvas.itemconfig(navigators.valid_input,text='Invalid input')
        window.update()

        return
        
    ha = EQ2_EQ1(target_RA,T0)
    alt = EQ1_AZ(ha,target_DEC,T0)[1]

    if alt < 0: # if target is below the horizon, the telescope cannot observe it
        navigators.canvas.itemconfig(navigators.valid_input,text='Object below \nhorizon')
        window.update()
        return
        
    # if everything is normal, the target change runs

    Target["state"] = "disabled"
    Observe["state"] = "disabled"
    Tracking["state"] = "disabled"

    navigators.canvas.itemconfig(navigators.valid_input,text='')
    
    GoToTarget(Recta,Decl,target_RA,target_DEC,T0)

    Target["state"] = "normal"
    Observe["state"] = "normal"
    Tracking["state"] = "normal"

    print(f"Target changed to: RA: {Recta:.3f}° DEC: {Decl:.3f}°")
    

def obs():
    """ Starts an observation """

    global is_Standby
    global Recta
    global Decl

    print(f"Observing at: RA: {Recta:.3f}° DEC: {Decl:.3f}°")

        
    try: # gets FOV
        f = float(navigators.Field_input.get().replace(',','.').replace(' ','').replace('-','')) # avoiding misspelled FOV
        f = abs(f) # correction for negative inputs if the previous didn't work
        
        
    except: # if negative string is not the problem
        navigators.canvas.itemconfig(navigators.valid_input,text='Invalid input')
        window.update()

        return
    
    # if everything is normal, the observation runs

    Target["state"] = "disabled"   
    Observe["state"] = "disabled"
    Tracking["state"] = "disabled"  
    
    Observation(Recta,Decl,f)
    navigators.canvas.itemconfig(navigators.valid_input,text='')

    Target["state"] = "normal"
    Observe["state"] = "normal"
    Tracking["state"] = "normal"

def toggle_tracking():

    global is_Standby
    global Azimuth # when tracking off telescope remains at fixed azimuthal coords
    global Altitude # when tracking off  telescope remains at fixed azimuthal coords

    global Recta
    global Decl
    #global T0

    is_Standby = not(is_Standby)

    if is_Standby:
        Tracking['text'] = 'Tracking ON'
        Recta,Decl = AZ_EQ1(Azimuth,Altitude,T0)
    else:
        Tracking['text'] = 'Tracking OFF'
        Azimuth, Altitude = EQ1_AZ(Recta,Decl,T0)

    window.update()

Target = Button(navigators.canvas,text='Go to target', command=get_target)
Observe = Button(navigators.canvas,text='Start observation', command=obs)
Tracking = Button(navigators.canvas,text='Tracking ON', command=toggle_tracking)

Target.place(x=80,y=350,anchor='center')
Observe.place(x=80,y=400,anchor='center')
Tracking.place(x=80,y=155,anchor='center')
############################################################


################### MAIN LOOP ###########################
while True:

    if is_Standby:
        follow(Recta,Decl,T0)

    else:
        Recta,Decl = AZ_EQ1(Azimuth,Altitude,T0)
        HourAngle = EQ2_EQ1(Recta,T0)
        
        navigators.update_all(Azimuth,Altitude,HourAngle,Recta,Decl) # updates the displayed coordinates
        b.refresh(T0) # refreshes infobar time. If tracking is off, the system counts time half as fast, this is the reason for the 2 factor

        # VERY SLOW ROTATION OF STARMAP
        top_section.rotate(angle=0.01,current=(Azimuth,Altitude),axis=0)  # rotates starmap left/right

        sleep(0.01)

    T0 += timedelta(seconds=timescale/10)
    window.update()
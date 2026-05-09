from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord

class ControlPanel:
    def __init__(self,root,azimuth=0,alt=0,HourA=0,Decl=0,LST=0):
        self.lat = np.radians(53+11/60+24/3600)
        self.root = root

        self.add_to_GUI(azimuth,alt,HourA,Decl,LST)

    def add_to_GUI(self,AZ,H,HA,DEC,LST):
        canvas = Canvas(self.root,bg='white',highlightbackground = 'black')
        self.X = 800*0.8
        self.Y = 800*0.4
        canvas.place(x=self.X, y=self.Y, relwidth=0.2, relheight=0.8)

        self.canvas = canvas

        self.text(AZ,H,HA,DEC,LST)
        self.target_entry()

    def text(self,AZ,H,HA,DEC,LST):
        canvas = self.canvas

        self.AZ_label = canvas.create_text(15,20,text=f'AZ: {AZ:.3f}',anchor='w')
        self.H_label = canvas.create_text(15,40,text=f'H:  {H:.3f}',anchor='w')

        self.HA_label = canvas.create_text(15,80,text=f'HA: {HA:.3f}',anchor='w')
        self.RA_label = canvas.create_text(15,100,text=f'RA: {LST-HA:.3f}',anchor='w')
        self.DEC_label = canvas.create_text(15,120,text=f'DEC:  {DEC:.3f}',anchor='w')

        self.valid_input = canvas.create_text(80,430,text='',fill='red',anchor='n')
    
    
    def target_entry(self):

        self.canvas.create_line(0,180,800*0.2,180,width=2)

        self.canvas.create_text(5,200,text="Target coordinates\n in degrees:",anchor='w')

        self.canvas.create_text(15,250,text="RA:",anchor='w')
        self.canvas.create_text(15,280,text="Decl:",anchor='w')
        self.canvas.create_text(15,310,text="Field:",anchor='w')

        self.RA_input = Entry(self.canvas,width=8)
        self.DEC_input = Entry(self.canvas,width=8)
        self.Field_input = Entry(self.canvas,width=8)
        self.RA_input.insert(0,"0")
        self.DEC_input.insert(0,"0")
        self.Field_input.insert(0,"1")

        self.RA_input.place(x=60,y=250,anchor='w')
        self.DEC_input.place(x=60,y=280,anchor='w')
        self.Field_input.place(x=60,y=310,anchor='w')


    def update_all(self,AZ,H,HA,RA,DEC):

        t = (HA%360)*240
        ra = (RA%360)*240

        ha = f"{t//3600:.0f} : {(t)%3600//60:.0f} : {(t)%60:.1f}"
        ra = f"{ra//3600:.0f} : {ra%3600//60:.0f} : {ra%60:.1f}"

        self.canvas.itemconfig(self.AZ_label,text=f'AZ: {(AZ+360)%360:.3f}')
        self.canvas.itemconfig(self.H_label,text=f'H:  {H:.3f}')

        self.canvas.itemconfig(self.HA_label,text=f'HA: {ha}')
        self.canvas.itemconfig(self.RA_label,text=f'RA: {ra}')
        self.canvas.itemconfig(self.DEC_label,text=f'DEC:  {DEC:.3f}')
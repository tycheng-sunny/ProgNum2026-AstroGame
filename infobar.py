from tkinter import *
from datetime import datetime,timedelta

class InfoBar:
    def __init__(self,root,time):
        bar = Canvas(root,highlightbackground= 'black',highlightthickness=3)
        bar.place(relheight=0.08,relwidth=1)

        bar.create_text(20,25,text="Place: Groningen\tCoords: 53°13'9.01\"N, 6°34'0.01\"E",anchor="w")

        #time = time + timedelta(hours=2)

        self.tbar = bar.create_text(20,40,text=f"Date: {time.date()} \tLocal time: {time.time().replace(microsecond=0)}",anchor="w")
        self.state = bar.create_text(500,15,text="Mode: STANDBY",anchor="nw",font=60)
        self.countdown = bar.create_text(550,45,text="",anchor="w",font=10)

        self.time = time
        self.bar = bar
        self.date = time.date()
        self.root = root

    def refresh(self,time,obs = False,timer=0):
        self.time = time
        self.bar.itemconfig(self.tbar,text=f"Date: {self.date} \tLocal time: {self.time.time().replace(microsecond=0)}")

        if obs:
            self.bar.itemconfig(self.countdown, text=f"Remaining: {10-timer:.2f} s")

        else:
            self.bar.itemconfig(self.countdown, text="")
        self.root.update()

    def change_mode(self,mode): # mode: (str) standby/observation/Changing target
        self.bar.itemconfig(self.state,text=f"Mode: {mode.upper()}")
        self.root.update()
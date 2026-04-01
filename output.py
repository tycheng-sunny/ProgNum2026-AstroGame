from matplotlib.pyplot import figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import numpy as np


class Output:
    def __init__(self,root):
        self.root = root
        print(self.root)
        self.fig = figure()
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.exists = False

        self.add_to_GUI()

    def add_to_GUI(self):
        bg = Canvas(self.root,background='grey',highlightbackground = 'black')
        bg.place(rely=0.4,relheight=0.7,relwidth=0.8)

        bg.create_rectangle(800*0.4-200,800*0.35-50,800*0.4+200,800*0.35+50,fill='white')
        self.info = bg.create_text(800*0.4,800*0.35,anchor='center',text="No output to display",font=20)

        self.bg = bg

    def add_output(self,image):
        image = np.asarray(image)
        self.exists = True
        self.canvas = FigureCanvasTkAgg(self.fig,master=self.root).get_tk_widget()
        self.canvas.place(rely=0.45,relx=0.05,relheight=0.5,relwidth=0.7)

        ax = self.fig.add_subplot()

        ax.imshow(image, interpolation='none', origin='lower',cmap="gray")
        ax.set_title('Observation')
        ax.set_xticks([])
        ax.set_yticks([])

        self.ax = ax

        self.root.update()

    def clear_output(self):
        self.bg.itemconfig(self.info,text="No output to display")
        if self.exists:
            self.canvas.destroy()
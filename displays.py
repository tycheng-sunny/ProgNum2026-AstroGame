from matplotlib.pyplot import figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Ellipse,Rectangle
from tkinter import *

import numpy as np


class DSP_Panels:
    def __init__(self,root,starting_position =(0,0)):

        self.fig = figure()
        self.stars= self.fig.add_subplot(1,3,1)
        self.front= self.fig.add_subplot(1,3,2)
        self.top= self.fig.add_subplot(1,3,3)
        self.fig.tight_layout()
    
        self.stars.set_aspect('equal')
        self.top.set_aspect('equal')
        self.front.set_aspect('equal')

        nStar = np.random.randint(20,30)
        self.starpos = np.array([np.random.random(nStar),np.random.random(nStar)])
        self.starsize = np.random.random(nStar)

        self.root = root

        self.add_to_GUI()
        self.display(azimuth=starting_position[0],altitude=starting_position[1])


    def add_to_GUI(self):

        self.canvas = FigureCanvasTkAgg(self.fig,master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(y=20,relwidth=1.0, relheight=0.4)
        self.canvas.get_tk_widget().config(highlightbackground = 'black')

    def display(self,azimuth,altitude):

        AZ = np.radians(azimuth)
        H = np.radians(altitude)


        ax = self.stars
        ax.cla()
        ax.set_xlabel('Sky section')
        ax.scatter(self.starpos[0],self.starpos[1],color='black',s=self.starsize)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
        ax.add_patch(Rectangle(xy=(0.4,0.4),width=0.2,height=0.2,fill=False,linestyle='--'))
        ax.axvline(x=0.5,linestyle='--',linewidth=0.5,color='black')
        ax.axhline(y=0.5,linestyle='--',linewidth=0.5,color='black')

        ax = self.top
        ax.cla()
        ax.set_xlabel('Top view of\nthe telescope')
        ax.add_patch(Ellipse(xy=(0,0),height=2*0.8,width=2*0.8,fill=False,linestyle='--',color='b'))

        ax.text(x=0,y=0.95,s="N",horizontalalignment='center',verticalalignment='center')
        ax.text(x=0,y=-0.95,s="S",horizontalalignment='center',verticalalignment='center')
        ax.text(x=0.95,y=0,s="E",horizontalalignment='center',verticalalignment='center')
        ax.text(x=-0.95,y=0,s="W",horizontalalignment='center',verticalalignment='center')
        
        ax.annotate("",xytext=(0,0),xy=(0.8*np.sin(AZ),0.8*np.cos(AZ)),arrowprops=dict(arrowstyle="->",color='blue'))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(-1.1,1.1)
        ax.set_ylim(-1.1,1.1)

        ax = self.front
        ax.cla()
        ax.set_xlabel('Front view of\nthe telescope')
        ax.add_patch(Ellipse(xy=(0,0),height=2*0.9,width=2*0.9,fill=False,linestyle='--',color='r'))
        ax.text(x=0,y=1.8,s="Z",horizontalalignment='center',verticalalignment='center')
        ax.annotate("",xytext=(0,0.1),xy=(0.8*np.cos(H),0.8*np.sin(H)+0.1 if np.sin(H) > 0 else 0.1),arrowprops=dict(arrowstyle="->",color='red'))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(-1,1)
        ax.set_ylim(0,2)

        self.canvas.draw()


    def rotate(self,angle,current=(0,0),axis=0):
        """
            axis: (int) 0 = azimuthal, 1 = vertical axis
            angle: (float) IN DEGREES the angle of rotation wanted
        """

        if axis == 0:
            self.starpos[0] -= angle*0.01

            for i in range(len(self.starpos[0])):
                if self.starpos[0][i] > 1:
                    self.starpos[0][i] = 0-np.random.random()
                    self.starpos[1][i] = np.random.random()
                    self.starsize[i] = np.random.random()

                elif self.starpos[0][i] < 0:
                    self.starpos[0][i] = 1+np.random.random()
                    self.starpos[1][i] = np.random.random()
                    self.starsize[i] = np.random.random()

        elif axis == 1:
            self.starpos[1] -= angle*0.05

            for i in range(len(self.starpos[1])):
                if self.starpos[1][i] < 0:
                    self.starpos[1][i] = 1+np.random.random()
                    self.starpos[0][i] = np.random.random()
                    self.starsize[i] = np.random.random()

                elif self.starpos[1][i] > 1:
                    self.starpos[1][i] = 0-np.random.random()
                    self.starpos[0][i] = np.random.random()
                    self.starsize[i] = np.random.random()

        self.display(current[0],current[1])
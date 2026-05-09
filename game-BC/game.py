#!/usr/bin/env python
# coding: utf-8

# In[115]:


import numpy as np
import os
import matplotlib.pyplot as plt
import imageio.v2 as imageio
from astropy.io import fits

class game:
    """integrals many ways"""
    def __init__(self):
        print('Loading')
    def rules(self):                 # Set mode to reading data
        f = open('rules.txt', 'r')
        contents = f.read()
        f.close()
        print(contents)
        
class Fun:
    def __init__(self):
        fun=int(np.random.random(1)*20)
        self.fun=fun
    def regen(self):
        self.fun=int(np.random.random(1)*20)
    def value(self):
        return self.fun

astrog=game()
fun=Fun()

print('Welcome to Astroguesser!')
print('Would you like to know the rules?')
ans = input()
if ans.lower() == 'yes':
    astrog.rules()
elif ans.lower() == 'fun':
    print(fun.value())
print("Let's get started! :D")


class ran_gal:
    def __init__(self):
        contents = os.listdir('images')
        contents=[i for i in contents if i[0]!='.']
        ind=int(np.random.random()*(len(contents)))
        self.contents=contents
        self.ind=ind
        self.name= contents[ind]
        
    def name (self):
        return self.name
        
    def image(self):
        images = os.listdir(f'images/{self.contents[self.ind]}')
        ind=int(np.random.random()*(len(images)))
        self.file=images[ind]
        
    def file(self):
        return self.file

gal=ran_gal() 
gal.image()

script_dir = os.path.dirname('game.ipynb') #<-- absolute dir the script is in
rel_path = f"images/{gal.name}/{gal.file}"
abs_file_path = os.path.join(script_dir, rel_path)

if gal.file[gal.file.find('.'):].lower() == '.fits':
    hdulist = fits.open(abs_file_path)
    hdr = hdulist[0].header 
    dat = hdulist[0].data
    plt.imshow(dat,origin="lower")
    plt.axis('off')
    plt.show()
else:
    f=imageio.imread(abs_file_path)
    plt.imshow(f,origin="lower")
    plt.axis('off')
    plt.show()

print("So which galaxy do you think this is?")    

letters=['A','B','C']
contents = os.listdir('images')
contents=[i for i in contents if i[0]!='.']

for i in range(len(contents)):
    print(f"{letters[i]}. {contents[i]}") 

guess=input()
if contents[letters.index(guess)]==gal.name:
    print('congrats')
else:
    print("better luck next time")

if fun.value()<11:
    print("Fun fact!")
    f = open('fun_facts.txt', 'r')
    lineCounter = 0
    with open('fun_facts.txt','r') as f:
        for line in f:
            lineCounter += 1
            if lineCounter == fun.value():
                print(line, end='')


# In[ ]:





# In[ ]:





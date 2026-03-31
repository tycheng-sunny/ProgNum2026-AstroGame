#!/usr/bin/env python
# coding: utf-8

# In[41]:


import random

stop = "no"
gold = 100

class Pop:

    def hdul():
        import numpy as np
        from astropy.io import fits
        from scipy import stats as st
        import matplotlib.pyplot as plt
        hdul = fits.open('./ngc6946.fits')
        hdul.info()
        data = hdul[0].data
        header = hdul[0].header
        
        fig, axis = plt.subplots(5,10,figsize = (15,8))
        zind = list(range(1,101,2))  #indices of z
        
        for i, axes in enumerate(axis.flat):
            z = zind[i]
            axes.imshow(data[z,:,:], origin = 'lower')
        
            axes.set_xticklabels([])
            axes.set_yticklabels([]) 
        plt.tight_layout()
        plt.show()
        
        zmin,zmax = 20,80
        
        himap = np.sum(data[zmin:zmax,:,:],axis = 0)
        plt.imshow (himap, origin = 'lower')
        plt.title( 'Total HI map')
        plt.xlabel(header['CTYPE1'])
        plt.ylabel(header['CTYPE2'])
        
        colourb = plt.colorbar()
        colourb.set_label(header['BUNIT'])
        plt.show()
        
        pvmap = data[:,:,50]  #the z and y
        
        plt.imshow(pvmap,origin = 'lower', aspect = 'auto')
        plt.axhline(40)
        
        plt.xlabel(header['CTYPE3'])
        plt.ylabel(header['CTYPE2'])
        plt.title('PV diagram')
        plt.show()
        
        spect = data[:,40,50]
        plt.plot(spect,color = 'limegreen')
        plt.xlabel(header['CTYPE3'])
        plt.ylabel(header['BUNIT'])
        plt.title('Global HI')
        
        plt.show()

    def SDSS():
        import numpy as np
        from astropy.io import fits
        from scipy import stats as st
        import matplotlib.pyplot as plt
        import pandas as pd
        from astropy.table import Table
        
        hdul = fits.open('SDSS_DR17_galaxies.fits')
        table = Table(hdul[1].data)
        df = table.to_pandas() 
        hdul.close()
        
        filters = ['u','g','r','i','z']  #sdss filters
        df = df [filters]  #keeping only the filters columns
        
        df = df[(df > 0 ).all(axis = 1)]  #only rows where all values are positive
        
        colours = pd.DataFrame()  #empty datafram for colours
        
        for i in range(len(filters)):
            for j in range(i + 1, len(filters)):  #no duplicates
                f1 = filters[i]
                f2 = filters[j]
        
                colourname = f'{f1}--{f2}'  #creates colors name like u-g
                colours[colourname] = df[f1] - df[f2]  #color difference
        
        m = colours.mean()
        s = colours.std()
        
        n =len(colours.columns)  #number of color combinations
        fig,axes = plt.subplots(n,n,figsize = (12,12))
        if n == 1:  #every subplot case
            axes = np.array([[axes]])
        
        for i in range(n):
            for j in range(n):
                ax =axes[i,j]
                coli = colours.columns[i]
                colj = colours.columns[j]
        
                if i == j:
                    ax.hist (colours[coli],bins = 30, color = 'limegreen')
                    mean = m[coli]
                    std = s[coli]
        
                    ax.set_xlim(mean - 3*std, mean + 3*std)  #setting the x limits
                    ax.set_title(f'{coli}, nu = {mean:.1f}, standart deviation = {std:.1f}',fontsize = 9)
                else:
                    ax.scatter(colours[colj], colours[coli], s = 1)
                    ax.set_xlim(m[colj] - 3*s[colj], m[colj] + 3*s[colj])
                    ax.set_ylim(m[coli] - 3*s[coli], m[coli] + 3*s[coli])
                ax.set_xticks([])
                ax.set_yticks([])
        
        plt.show()

    def blup():
        import numpy as np
        from astropy.io import fits
        from scipy import stats as st
        import matplotlib.pyplot as plt
        from astropy.visualization import ImageNormalize
        from astropy.visualization import SinhStretch, AsymmetricPercentileInterval, LinearStretch,\
                                          LogStretch, PowerStretch, SqrtStretch, SquaredStretch,\
                                          HistEqStretch, ZScaleInterval
        
        
        def imdisplay(data,
                      ax,
                      vmin=None, vmax=None,
                      percentlow=1, percenthigh=99,
                      zscale=False,
                      scale='linear',
                      power=1.5,
                      cmap='gray',
                      **kwargs):
            if zscale:
                # Always overwrite vmin and vmax
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
            if scale == 'asinh':
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
                stretch = HistEqStretch(data)  # Needs argument data and data min, max for vmin, vmax
                vmin = data.min(); vmax = data.max()
        
            norm = ImageNormalize(vmin=vmin, vmax=vmax, stretch=stretch)
            return ax.imshow(data, interpolation='none', origin='lower', norm=norm, cmap=cmap, **kwargs)
        
        hdul = fits.open ('20210422_Li_.00000066.FIT')
        
        data = hdul[0].data
        hdul.close()
        
        #list of scales options
        scales = ['linear','log','sqrt','asinh','power']   #adjusts based on imdisplay available
        scales = [None] + scales
        
        n = len(scales)  #number of plots
        
        fig, axes = plt.subplots(1,n,figsize = (4*n,4))  #creating subplots in 1 row
        
        if n == 1:
            axes = [axes]
        
        for i, scale in enumerate(scales):
            ax = axes[i]
        
            if scale is None:
                imdisplay(data, ax = ax)
                ax.set_title('No scaling', fontsize = 10)
            else:
                imdisplay(data, ax = ax, scale = scale)
                ax.set_title(f'Scale: {scale}',fontsize = 10)
        plt.tight_layout()
        plt.show()

    def graph():
        import math
        import numpy as np
        from matplotlib.pyplot import subplots, show
        from astropy.io import fits
        
        hdul = fits.open('./ngc6946.fits') 
        data = hdul[0].data
        header = hdul[0].header
        
        perfil = data[:,55,58]
        v = np.linspace(233,377,len(perfil))
        
        fig, ax = subplots()
        ax.plot(v,perfil,color = 'lime')
        ax.set_xlabel(header.get('CUNIT3', '$km/s$'))
        ax.set_ylabel(header.get('BUNIT', '$Brightness$'))
        ax.set_title ('$HI \ Profile$')
        show()

    def m101():
        from imageio import imwrite, imread
        from matplotlib.pyplot import figure, show
        import numpy as np
        
        m101 = imread("m101BW.jpg")
        imwrite('myimage.png', m101) 
        
        fig = figure()
        frame = fig.add_subplot(1,1,1)
        m101 = imread('myimage.png')
        
        imageObject = frame.imshow(m101, cmap='jet')
        fig.colorbar(imageObject, ax=frame, fraction=0.046, pad=0.04) 
        frame.contour(m101, levels=np.percentile(m101, [90]), colors='y')
        show()
        
class Cardvalue:
    
    def __init__(self,card):
            self.card = card
        
    def card_value_player(card):
        if card[0] in ['Jack', 'Queen', 'King']:
            return 10
        elif card[0] == 'Ace':
            a = int(input("You got an Ace do u want to treat it as a 1 or 11"))
            return a
        else:
            return int(card[0])
        
    def card_value_dealer(card):
        if card[0] in ['Jack',   'Queen', 'King']:
            return 10
        elif card[0] == 'Ace':
            if dealer_score <= 10:
                a = 11
            else:
                a = 1
            return a
        else:
            return int(card[0])

while stop == "no":
    print("You have ", gold, " stars")
    bet = int(input("How many do you want to bet"))
    Pop.hdul()
    if bet < 50:
        print(f'Only {bet}... you sure? That is a little pathetic.')
        bet = int(input("How much do you ACTUALLY want to bet"))
        if bet < 50:
            print("Coward...")
    while bet > gold:
        print("You are not that rich")
        bet = int(input("How much do you ACTUALLY want to bet"))
    
    card_categories = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    deck = [(card, category) for category in card_categories for card in cards_list]
    
    random.shuffle(deck)
    player_card = [deck.pop(), deck.pop()]
    dealer_card = [deck.pop(), deck.pop()]
    Pop.SDSS()
    while True:
        player_score = sum(Cardvalue.card_value_player(card) for card in player_card)
        dealer_score = sum(Cardvalue.card_value_dealer(card) for card in dealer_card)
        print("Cards Player Has:", player_card)
        print("Score Of The Player:", player_score)
        print("\n")
        print(dealer_card)
        print("Score Of The Dealer:", dealer_score)
        Pop.blup()
        print("\n")
        choice = input('What do you want? ["play" to request another card, "stop" to stop]: ').lower()
        if choice == "play":
            new_card = deck.pop()
            player_card.append(new_card)
            player_score = sum(Cardvalue.card_value_player(card) for card in player_card)
            print("\n")
            if player_score > 21:
                break
        elif choice == "stop":
            break
        else:#4
            print("Invalid choice. Please try again.")
            continue
    
    while dealer_score < 17:
        new_card = deck.pop()
        dealer_card.append(new_card)
        dealer_score += Cardvalue.card_value_dealer(new_card)
    
    print("Final score of dealer:", dealer_score)
    print("Final score of player:", player_score)
    Pop.graph()
    if dealer_score <= player_score:
        if player_score <= 21:
            print("Dumb luck...")
            gold += 2*bet
        else:
            print("How does it feel to be bad at gambling?")
            gold -= bet
    else:
        if dealer_score >= player_score:
            if player_score <= 21:
                if dealer_score <=21:
                    print("How does it feel to be bad at gambling?")
                    gold -= bet
                elif dealer_score == player_score:
                    print("How does it feel to be bad at gambling?")
                    gold -= bet
                else:
                    print("Dumb luck...")
                    gold += 2*bet 
            else:
                print("How does it feel to be bad at gambling?")
                gold -= bet
    Pop.m101()
    print("Current Star Value: ", gold)
    if gold <= 0:
        stop = "yes"
    else:
        stop = input("Do you want to stop? (yes or no)")
    

if gold < 100 and gold > 0:
    print("Your mom comes into the room...")
    print("You lost money again???")
    print("What is wrong with you???????")
elif gold == 0:
    print("You are a failure.")
else:
    print("You are banned")


# In[ ]:





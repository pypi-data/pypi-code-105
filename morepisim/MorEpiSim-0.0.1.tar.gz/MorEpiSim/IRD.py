

import matplotlib.pyplot as plt
import numpy as np
import random


global fig3, ax1, Is, Rs, Ds
fig3 = plt.figure(figsize=(9,6))
ax1 = fig3.add_subplot(111)

Is = []
Rs = []
Ds = []
def plot_ird(I, R, D, ep, step, reward, R0, show, save):
    global fig2, ax1, Is, Rs, Ds

    plt.style.use('fivethirtyeight')

    Is.append(I)
    Rs.append(R)
    Ds.append(D)
    
    ax1.cla()

    #uncoment thus if u want to update the viewed frame interval
    #plt.xlim(ep*50, (ep+2)*50)

    ax1.axvline(x=(ep)*50, color='black', linestyle='--', linewidth=0.8)
    ax1.axvline(x=(ep+1)*50, color='black', linestyle='--', linewidth=0.8)

    ax1.plot (Is, 'r.-', linewidth=0.5, label="Infected")
    ax1.plot (Rs, 'g.-', linewidth=0.5, label="Recovered")
    ax1.plot (Ds, 'b.-', linewidth=0.5, label="Deaths")

    plt.legend(loc='upper left')

    R0 = float("{:.3f}".format(R0))
    ax1.set_title('episode= '+str(ep)+ ' | step= '+str(step) +' | R0= '+str(R0)
                  + ' | reward= '+str(reward),
              ha="center", va="bottom", size=10, color="orange") 

    if show==True:
        plt.ion()
        fig3.show() 
        plt.pause(0.0000001)
    if save==True:
        return fig3
    else:
        pass



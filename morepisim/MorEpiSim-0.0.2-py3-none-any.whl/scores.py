

import matplotlib.pyplot as plt
import numpy as np
import random


global fig2, ax1, ax2, h_scores, e_scores
fig2 = plt.figure(figsize=(12,6))
ax1 = fig2.add_subplot(211)
ax2 = fig2.add_subplot(212)

h_scores = []
e_scores = []

def plot_scores(h_score, e_score, ep, step, reward, R0, Te, show, save):
    global fig2, ax1, ax2, h_scores, e_scores


    plt.style.use('fivethirtyeight')
    #plt.style.use('Solarize_Light2')

    if  h_score > -1: 
        h_scores.append(h_score)
    else:
        h_scores.append(-0.1)
    ax1.cla()
    #ax1.axhline(y=0.5, color='y', linestyle='--')
    ax1.axvline(x=(ep)*50, color='black', linestyle='--')
    ax1.axvline(x=(ep+1)*50, color='black', linestyle='--')
    ax1.plot (h_scores, 'r.-', linewidth=0.5)

    R0 = float("{:.3f}".format(R0))
    h_score = float("{:.3f}".format(h_score))
    ax1.set_title('episode= '+str(ep)+ ' | step= '+str(step) +
                  ' | health score = '+str(h_score)+ ' | R0= '+str(R0)
                  + ' | reward= '+str(reward),
              ha="center", va="bottom", size=10, color="orange") 

    e_scores.append(e_score) 
    ax2.cla()
    ax2.axhline(y=Te, color='y', linestyle='--')
    ax2.axvline(x=(ep)*50, color='black', linestyle='--')
    ax2.axvline(x=(ep+1)*50, color='black', linestyle='--')
    ax2.plot (e_scores, 'b.-', linewidth=0.5)
    e_score = float("{:.3f}".format(e_score))
    ax2.set_title('episode= '+str(ep)+ ' | step= '+str(step) +
                  ' | economy score= '+str(e_score) + ' | R0= '+str(R0)
                  + ' | reward= '+str(reward),
              ha="center", va="bottom", size=10, color="orange") 

    if show==True:
        plt.ion()
        fig2.show() 
        plt.pause(0.0000001)
    if save==True:
        return fig2
    else:
        pass



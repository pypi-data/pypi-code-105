
# with scores plot
import networkx as nx 
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import random

global ax, fig, G, l1, l2, l3, l4, l5, l6, l7, l8, edgelist, pos, e_pos
fig, ax = plt.subplots(figsize=(10,7))
G = nx.DiGraph()
l1, l2, l3, l4, l5, l6, l7, l8, l9 ='Cur_I', 'N', 'Frst_I', 'Re_I', 'Nxt_I', 'U', 'K', 'R', 'D'
edgelist= [(l1,l2),(l2,l3),(l2,l4),(l3,l5),(l5, l6),(l5, l7),(l7, l8),(l7, l9), (l6, l1), (l8,l2)]

pos = {l1: (10, 80), l2: (10, 50), l3:(60, 50), l4:(10, 20),  #I, N, FI, RI
       l5:(100, 50), l6:(150, 80), l7:(150, 20), l8:(100,20), l9:(200, 20) #NI, U, K, R, D
       }

e_pos = {l1: (10, 80), l2: (10, 50), l3:(60, 50), l4:(10, 20),  #I, N, FI, RI
       l5:(100, 50), l6:(150, 80), l7:(150, 20), l8:(100,20), l9:(200, 20) #NI, U, K, R, D
       }
def showNet(ep, step, states, quantities, h_score, e_score, reward, R0, show, save):
    global ax, fig, G, l1, l2, l3, l4, l5, l6, l7, l8, I9, edgelist, pos, e_pos

    #plt.style.use('fivethirtyeight')
    #plt.style.use('Solarize_Light2')
    
    fig.clf()            
        
    s1 = float("{:.3f}".format(states[0]))
    s2 = float("{:.3f}".format(states[1]))
    s3 = float("{:.3f}".format(states[2]))
    s4 = float("{:.3f}".format(states[3]))
    
    e_labels = [s1, s4, float("{:.3f}".format(1-s2)), s2, float("{:.3f}".format(1-s3)), s3]
    
    edge_labels = {(l2,l3):e_labels[0],(l2,l4):e_labels[1], (l5,l6):e_labels[2],
                   (l5, l7):e_labels[3],(l7,l8):e_labels[4], (l7,l9):e_labels[5]}

    nx.draw_networkx_nodes(G, pos=pos, nodelist=list(pos.keys()), node_size=2000, alpha=1)
                                                                        #put here, connectionstyle="arc3,rad=0.1" for curved edges
    nx.draw_networkx_edges(G, pos=e_pos, edgelist= edgelist , edge_color="gray",
                           arrows=True, arrowsize=20, node_size=2000, alpha=1) #arrowstyle='-|>' or 'wedge'

    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels, font_size=10) 
    nx.draw_networkx_labels(G, pos=pos, labels=dict(zip(pos.keys(),pos.keys())),  font_color="black") 
    
    xx = list(pos.values())
    # Cur_I
    x,y= xx[0]
    popul_Cur_I = int(quantities[0])
    plt.text(x,y-4.6,s= popul_Cur_I, fontsize=10, bbox=dict(facecolor='yellow', alpha=0.6),horizontalalignment='center')

    # N
    x,y= xx[1]
    popul_N = int(quantities[1])
    plt.text(x,y-4.6,s= popul_N, fontsize=10, bbox=dict(facecolor='yellow', alpha=0.6),horizontalalignment='center')

    # F_I
    x,y= xx[2]
    popul_FI = int(quantities[2])
    plt.text(x,y-4.6,s= popul_FI, fontsize=10, bbox=dict(facecolor='yellow', alpha=0.6),horizontalalignment='center')

    # Re_I
    x,y= xx[3]
    popul_ReI = int(quantities[3])
    plt.text(x,y-4.6,s= popul_ReI, fontsize=10, bbox=dict(facecolor='yellow', alpha=0.6),horizontalalignment='center')

    # Nxt_I
    x,y= xx[4]
    popul_NI = int(quantities[4])
    plt.text(x,y-4.6,s= popul_NI, fontsize=10, bbox=dict(facecolor='yellow', alpha=0.6),horizontalalignment='center')
    
    # U
    x,y= xx[5]
    popul_U = int(quantities[5])
    plt.text(x,y-4.6,s= popul_U, fontsize=10, bbox=dict(facecolor='yellow', alpha=0.6),horizontalalignment='center')

    # K
    x,y= xx[6]
    popul_K = int(quantities[6])
    plt.text(x,y-4.6,s= popul_K, fontsize=10, bbox=dict(facecolor='yellow', alpha=0.6),horizontalalignment='center')

    # R
    x,y= xx[7]
    popul_R = int(quantities[7])
    plt.text(x,y-4.6,s= popul_R, fontsize=10, bbox=dict(facecolor='yellow', alpha=0.6),horizontalalignment='center')

    # D
    x,y= xx[8]
    popul_D = int(quantities[8])
    plt.text(x,y-4.6,s= popul_D, fontsize=10, bbox=dict(facecolor='yellow', alpha=0.6),horizontalalignment='center')

    R0 = float("{:.3f}".format(R0))
    h_score = "{:.3f}".format(h_score)
    e_score = "{:.3f}".format(e_score)
    
    plt.title('episode= '+str(ep)+ ' | step= '+str(step) + ' | health score= '+str(h_score) +
              ' | economy score= '+str(e_score) + ' | R0= '+str(R0) + ' | reward= '+str(reward), 
              ha="center", va="bottom", size=10, color="orange") 

    # Hide grid lines
    plt.grid(False)

    if save==True:
        return fig

    if show==True:
        plt.ion()
        fig.show() 
        plt.pause(0.0000001)

    else:
        pass

# Test:
##gg = showNet(10, 44, [11, 22, 33], [1, 2, 3, 4, 5, 6, 7],
##                    0.44, 0.55, show=False, save=True)


        


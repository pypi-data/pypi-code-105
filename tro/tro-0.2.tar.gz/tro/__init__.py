import numpy as np
import matplotlib.pyplot as plt

def tell():
    return ('Tro best dog guau guau.')

def TTT(opt = 'new'):
    if(opt == 'original'):
        plt.figure()
        plt.imshow(np.load('images/TTT_OG.npy'))
        plt.axis('off')
        plt.show()
    else:
        plt.figure()
        plt.imshow(np.load('images/TTT.npy'))
        plt.axis('off')
        plt.show()
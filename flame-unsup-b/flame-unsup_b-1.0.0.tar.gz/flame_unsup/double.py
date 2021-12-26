import matplotlib as mpl
# mpl.rcParams['mathtext.fontset'] = 'stix'
# mpl.rcParams['font.family'] = 'STIXGeneral'
import matplotlib.pyplot as plt
#import seaborn as sns  #not needed?


def jetParams():
    from jupyterthemes import jtplot  #configure Jupyter Notebook in order for it do display matplotlib plots according to the current                                             theme.
    jtplot.style()


def defParams():
    mpl.rcParams.update(mpl.rcParamsDefault) #default configuration

def setParams(ndef=22):
    plt.rc('xtick', labelsize=ndef)  #size of x coordinates
    plt.rc('ytick', labelsize=ndef)  #size of y coordinates
    plt.rc('axes', labelsize=ndef+2) #labelsize:Fontsize of the x and y labels
    plt.rc('legend',fontsize=ndef)   #legend generally appears as a box to the right or left of your graph.
    plt.rc('axes',titlesize=ndef)    #titlesize:Fontsize of the axes title
    # plt.rc('figure',figsize = (4,3))
#     plt.rc('figure',dpi = 360)

    # Get the best of both ggplot and seaborn
    # plt.style.use('ggplot')
    # plt.style.use('seaborn-deep')
#     plt.rcParams['figure.autolayout'] = True 
#     plt.rcParams['figure.dpi'] = 360

# plt.rc('text', usetex=True)

# mpl.rcParams['text.usetex']=True
# mpl.rcParams['text.latex.unicode']=True


# Get the best of both ggplot and seaborn
# plt.style.use('ggplot')
# plt.style.use('seaborn-deep')


def plotImg(M,cmap="jet",isgrid=None,saver=None,titler="Kurtosis",aspect=1,prior=' ',closer=True):  
#     plt.figure(figsize=(10,5))
    plt.imshow(M,cmap=cmap,aspect=aspect)#,extent=[0,0.36,0,0.36])
    plt.grid(isgrid)
    plt.xticks([])#np.arange(6,42,6)/100,rotation='vertical')
    plt.yticks([])#np.arange(0,42,6)/100)
    plt.title(titler,)
    plt.colorbar()
    plt.tight_layout()
    if saver!= None:
        plt.savefig(prior+ saver+".png", dpi = 480, #saver.png is created
                    transparent=True,
                   bbox_inches='tight',
                   pad_inches = 0.2)
    if closer:
        plt.close()
    else:
        plt.show()  
    
    
    


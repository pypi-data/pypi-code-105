import numpy as np
import os   #sys is not needed?
import matplotlib.pyplot as plt
import plotly.express as px    

# from utils import normalise, featurise

class LoadMPI():
    def __init__(self,fpath=0):
        self.inipath = "C:/Users/Dell/Downloads/verify/urmunsup/data1/aset/"
        if fpath==0:
            self.fpath = self.inipath
            self.loadFile("urmunsup")
        else:
            self.fpath = fpath
        
    def loadFile(self, val="urmunsup"):
        self.fpath = self.fpath.replace("urmunsup",val)
        flist = [f for f in os.listdir(self.fpath) if f.endswith(".mpi")] #list of files
        
        self.flist = sorted(flist, key=lambda f: float(f[-20:-10]) ) #sorted list of files, what is this f?
        self.file = self.flist[0]   #list[0]
        self.filer = open(self.fpath+self.file,"rb")  #opening a specific data file
        self.loadOptions()
        self.loadVariables()

    def loadOptions(self):  
        if "urmunsup" in self.fpath:
            self.nx = 672
            self.ny = 672
            self.badOffset = 0
            self.species = "varhcci.txt" #default data?
        else:
            self.nx = 3600
            self.ny = 1800
            self.badOffset = 89266
            self.species = "varisml.txt" #default data?
                
    def loadVariables(self,ipath="C:/Users/Dell/Downloads/verify/urmunsup/data1/aset/"): #ipath is default data?
#        ipath = "/home/shubham/Projects/Anomaly/src/unsup/"
        fr = open(ipath+self.species,"r")    #opens varhcci/varisml
        ychem = fr.read()                    #content of fr is stored in ychem
#         jack = raw.split()
#         sparo = [v for i,v in enumerate(jack) if (i+1)%3==0]
#         ychem = " ".join(sparo)
        ychem += " T P u v w"            
        variables = ychem.split(" ")       #returns a list

        self.idvar = {i:v for i,v in enumerate(variables)}   
        self.varid = {v:i for i,v in enumerate(variables)} # this is a dictionary
        self.variables = self.varid
        self.nv = len(variables)
        self.i = 0

    def selTime(self,index):
        ## path remains same just the file changes
        self.file = self.flist[index]
        self.filer = open(self.fpath+self.file,"rb")      #opening other data file

    def selSpec(self,index):
        
        ## file remains same, just index changes
        self.i = index
    
    def getDat(self,time):
        ### be careful with this function ; memory sensitive
        self.selTime(time)
        a = np.fromfile(self.filer,
                        count=self.nx*self.ny*self.nv,dtype="float64") #referring to second data file
        dat = a.reshape((self.nx,self.ny,self.nv),order="F") 
        return dat 
    
    def getHrr(self):
        n = self.file.find('E')   #n is the value of position of first 'E'
        root = self.file[n-6:n+4]  #slicing a second file
        a = np.fromfile(self.fpath[:-5]+"hrr/hrr."+root+".mpi",
                        count=self.nx*self.ny*1,dtype="float64") #is it applies to only particular input?
        dat = a.reshape((self.nx,self.ny,1), order="F") 
        return dat      
    
    def getMat(self):
#         i = self.variables[t]
        self.filer.seek(self.i*8*self.nx*self.ny+self.badOffset)  #sets the cursor
        a = np.fromfile(self.filer,
                        count=self.nx*self.ny,dtype="float64")
        T = a.reshape(self.nx,self.ny,order="F")        
        return T

    def getTrain(self, j):
        self.file = self.flist[j] 
        y = self.getHrr()  #data1
        x = self. getDat(j) #data2
        return x,y
    
    def stPlot(self,saver="C:/Users/Dell/Downloads/verify/urmunsup/data1/aset/temp.png"):
        T = self.getMat() #data 3
        plt.figure(figsize=(6,6))
        fig = plt.imshow(T,cmap = "jet",aspect=1)  #imshow() to plot
        plt.title(self.file)
        plt.colorbar()
        if saver!=0:
            plt.savefig(saver) #saves the plot
        plt.show()
        return fig
        
    def dyPlot(self):
        T = self.getMat() #data 3
        fig = px.imshow(T,
                        color_continuous_scale="jet",
                       title=self.file)
        fig.update_layout(
           autosize=False,
           width=800,
           height=800,)
        return fig

    


import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  ## to not create QApp without main thread
import matplotlib.pyplot as plt

import plotly.express as px

class loadmpi():
    def __init__(self):
        self.inipath = "C:/Users/Dell/Downloads/python_data_sets/data1/aset/" #is it default??
        self.fpath = self.inipath
        
    def loadFile(self, val):
        self.fpath = self.inipath.replace("data1",val)
        flist = [f for f in os.listdir(self.fpath) if f.endswith(".mpi")]
        self.flist = sorted(flist, key = lambda f: float(f[-20:-10]))
        self.file = self.flist[0]
        self.filer = open(self.fpath+self.file,"rb")
        
        self.loadOptions()
        self.loadVariables()

    def loadOptions(self):  
        self.nx = 1800
        self.ny = 3600
        self.badOffset = 89266
        self.species = "C:/Users/Dell/Downloads/python_data_sets/data1/aset/varisml.txt"
        self.asp = 0.6
        if "hcci" in self.fpath:
            self.nx = 672
            self.ny = 672
            self.badOffset = 0
            self.species = "C:/Users/Dell/Downloads/python_data_sets/data1/aset/varhcci.txt"
            self.asp = 1
    
    def loadVariables(self):
        fr = open(self.species,"r")
        ychem = fr.read()
#         jack = raw.split()
#         sparo = [v for i,v in enumerate(jack) if (i+1)%3==0]
#         ychem = " ".join(sparo)
        ychem += " T P u v w"
        variables = ychem.split(" ")

        self.idvar = {i:v for i,v in enumerate(variables)}
        self.varid = {v:i for i,v in enumerate(variables)}
        self.variables = self.varid
        self.i = 0

    def selTime(self,index):
        ## path remains same just the file changes
        self.file = self.flist[index]
        self.filer = open(self.fpath+self.file,"rb")

    def selSpec(self,index):
        ## file remains same, just index changes
        self.i = index
        
    def loadMat(self):
#         i = self.variables[t]
        self.filer.seek(self.i*8*self.nx*self.ny+self.badOffset)
        a = np.fromfile(self.filer,
                        count=self.nx*self.ny,dtype="float64")
        T = a.reshape(self.ny,self.nx,order="F")        
        return T

    def stPlot(self):
        T = self.loadMat()
#        plt.figure(figsize=(6,6))
        fig = plt.imshow(T,cmap = "jet",aspect=self.asp)
        plt.title(self.file)
        plt.colorbar()
        plt.savefig("temp.png")
        plt.close()
        return fig
        
    def dyPlot(self):
        T = self.loadMat()
        fig = px.imshow(T,
                        color_continuous_scale="jet",
                       title=self.file,
                       aspect=self.asp)
        fig.update_layout(
           autosize=False,
           width=800,
           height=800,)
        return fig

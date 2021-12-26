import os
import numpy as np
#import matplotlib.pyplot as plt #unused??

import plotly.express as px



filer = "C:/Users/Dell/Downloads/python_data_sets/data1/aset/" #default data??
flist = os.listdir(filer)
file1 = "hcci.4.0000E-06.field.mpi" #default data??

spec = ['H','H2','O','O2','OH','H2O','HO2','H2O2','CO','CO2','CH2O','HO2CHO','O2CHO','CH3O2H','CH3O2','CH4','CH3','C2H5','C2H4','C2H3','CH3CHO','C2H5OH','O2C2H4OH','N','NO','NO2','N2O','N2']
spec += ['T','P','u','v','w']

species = {s:i for i,s in enumerate(spec)}

nx = 672
ny = 672
nv = len(spec)
def getDat(file=file1):
    dat = np.fromfile(filer+file,count=nv*nx*ny,dtype="float64") #,offset=badHead+1*nx*ny)
    dat = dat.reshape((nx,ny,nv),order="F")
    tdat = dat.T
    return tdat

tdat = getDat()

def selSpec(index,titler):
    print(index)
    fig = px.imshow(tdat[index],
                    color_continuous_scale="jet",
                   title=titler)
    return fig

def selTime(index,jspec):
    filej = flist[index]    
    tdat = getDat(filej)
    return selSpec(jspec,titler=filej)






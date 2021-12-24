import os
import numpy as np
import torch

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

from flame_time.datagen import DataLoader
from flame_time.model import LSTM

datacolor = "royalblue"
dataName = "sample1"
dataPath = "C:/Program Files/" #default data??
data_f = DataLoader(dataPath+dataName+".csv")


modelPath = "/home/shubham/Academics/DAV/Project/notebooks/"
model = LSTM(num_classes=1, input_size=1, hidden_size=2, num_layers=1)
model.load_state_dict(torch.load(modelPath+"lstm.tch"))
model.eval() 



def predict(dat):
	y_pred = model(dat.X)

	data_predict = y_pred.data.numpy()
	data_predict = dat.sc.inverse_transform(data_predict)

	dataY_plot = dat.sc.inverse_transform(dat.Y.data.numpy())
	hold = dat.train_size
	return dataY_plot,data_predict[1:]

y1,y2 = predict(data_f)
### Generate Plots:--

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
fig.suptitle("Time Series Prediction -DAV")

#l = plt.axvline(x=dat.train_size, c='r', linestyle='--')
f, = ax.plot(y1,label="true") #,linestyle ='-',color="k",linewidth=3)
s, = ax.plot(y2,label="predicted") #,linestyle =':',color="k",linewidth=3)
plt.legend() #prop={'size': 15})


plt.xlabel("Time (units)")
plt.ylabel("Theta")
#ax.autoscale()


axcolor = 'lightgoldenrodyellow'
axcolor = 'azure'


rax = plt.axes([0.025, 0.3, 0.15, 0.35], facecolor=axcolor)
radio = RadioButtons(rax, ('airline', 'shampoo','birth',
						'temperatures','sunspots'), active=1)
def colorfunc(label):
	data2 = DataLoader(dataPath+label+".csv")
#	dat.__init__(dataPath+label+".csv")
	y1,y2 = predict(data2)
	changeLines(f,y1)
	changeLines(s,y2)
#	ax.relim()
radio.on_clicked(colorfunc)

def changeLines(l,x):
	l.set_xdata(range(len(x)))
	l.set_ydata(x)






plt.show()



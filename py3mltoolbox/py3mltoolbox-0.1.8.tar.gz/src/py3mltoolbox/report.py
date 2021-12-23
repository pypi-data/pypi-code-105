import os
import sys
import random
import py3toolbox as tb
import numpy as np
import matplotlib.pyplot as plt

from .dataset       import  *

def _get_output_files(key, output_folder):
  output_files = tb.get_files(output_folder)
  selected_files = []
  for f in output_files:
    if key in f:
      selected_files.append(f)

  selected_files.sort()
  return selected_files



def preview_images(data, labels, count=10, output_folder=None):
  """
    Data is numpy array, transform to image and save 
  
  """  
  preview_files = []
  for i in range(1,count+1):
    preview_index = random.choice(range(1,len(data)+1))
    plt.clf()
    plt.title(str(labels[preview_index]))
    plt.imshow(data[preview_index], interpolation='nearest')
    plt.tight_layout()
    preview_file = output_folder + "/preview_" + str(preview_index) + "." + str(labels[preview_index]) + ".png"
    plt.savefig(preview_file)
    preview_files.append(preview_file)
    plt.clf()  
    




def plot_decision_boundary(model = None, dataset = None, X = None, Y = None, title = "Train", output_folder=None):
  """
    model           : model object
    dataset         : single dataset object (Y is the last column)
    X               : X data
    Y               : Y data
    title           : Train / Test
  """

  # check input params
  assert model is not None, "model is required"
  
  # create model specific folder
  output_folder +=  "/" + model["name"]
  tb.mk_folder (output_folder)

  # parse dataset
  if dataset is not None:  X, Y  = parse_dataset(dataset)

  x_min = X[:,0].min(axis=0)[0,0]
  x_max = X[:,0].max(axis=0)[0,0]
  y_min = X[:,1].min(axis=0)[0,0]
  y_max = X[:,1].max(axis=0)[0,0]

  x_min -=  (x_max - x_min) / 20
  x_max +=  (x_max - x_min) / 20 
  y_min -=  (y_max - y_min) / 20  
  y_max +=  (y_max - y_min) / 20  

  h = (x_max - x_min + y_max - y_min ) / 400
  xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h), sparse=False)

  # predict values
  zz = np.asmatrix(model["model"].predict(x = np.c_[xx.ravel(), yy.ravel()], batch_size=32, workers=2, use_multiprocessing=True))
  zz = np.argmax(zz, axis =1)
  zz = zz.reshape(xx.shape)

  data_boundary_file = output_folder + "/decision.boundary." + title + ".jpg"

  # plot
  plt.clf()
  plt.tight_layout()
  fig = plt.figure(figsize=(1, 1))
  fig.set_figwidth(6)
  fig.set_figheight(6)
  subplt = fig.add_subplot()
  subplt.set_title(title)
  subplt.contourf(xx, yy, zz, cmap=plt.cm.Spectral)
  subplt.scatter(X[:, 0].tolist(), X[:, 1].tolist(), c = Y.tolist(),  marker="o",  s=25, edgecolor="k")
  if output_folder is not None:
    fig.savefig(data_boundary_file, dpi=200)
  else:
    plt.show()
  pass




def history_result(model, output_folder=None):

  # create model specific folder
  output_folder +=  "/" + model["name"]
  tb.mk_folder (output_folder)

  # set history
  history = model["history"]

  # collect training history data
  acc       = history.history['accuracy']
  val_acc   = history.history['val_accuracy']
  loss      = history.history['loss']
  val_loss  = history.history['val_loss']
  epochs    = range(len(acc))

  # draw history result
  plt.clf()
  fig = plt.figure()
  
  ax1 = fig.add_subplot(121)
  ax1.plot(epochs, acc, 'r', label='Train accuracy')
  ax1.plot(epochs, val_acc, 'b', label='Val accuracy')
  ax1.title.set_text('Train/Val Accuracy')
  ax1.set_xlabel('epoches')
  ax1.set_ylabel('Accuracy')
  ax1.legend()
  
  ax2 = fig.add_subplot(122)

  ax2.plot(epochs, loss, 'r', label='Train Loss')
  ax2.plot(epochs, val_loss, 'b', label='Val Loss')
  ax2.title.set_text('Train/Val Loss')
  ax2.set_xlabel('epoches')
  ax2.set_ylabel('Loss')
  ax2.legend()
  plt.tight_layout()
  if output_folder is not None:
    tb.write_file(file_name = output_folder + "/history.result.json", text=tb.pretty_json(history.history), mode="w")
    fig.savefig(output_folder + "/history.result.jpg")
  else:
    plt.show()


def gen_report(config=None, models=None):
  assert config is not None, "config cannot be None"
  assert models is not None, "models cannot be None"

  report_file   = config["output"] + "/report.html"
  total_models  = len(list(models.keys()))

  html = ""
  html += "<HTML>"
  html += "<BODY>"
  html += "<TABLE BORDER=1 WIDTH=1800>"

  # show dataset
  html += "<TR>"
  html += "<TD ALIGN=CENTER>Dataset</TD>"
  html += "<TD ALIGN=LEFT COLSPAN=" + str(total_models) + ">"
  html += "<PRE>" 
  html += tb.read_file(config["output"] + "/dataset.info.txt" )
  html += "</PRE>"
  html += "</TD>"
  html += "</TR>"


  # show preview
  if len(_get_output_files("preview", output_folder=config["output"])) >0 :
    html += "<TR>"
    html += "<TD ALIGN=CENTER>Preview</TD>"
    html += "<TABLE WIDTH=100%><TR>"
    for f in _get_output_files("preview", output_folder=config["output"]):
      html += "<TD ALIGN=CENTER>" 
      html += "<IMG SRC='" + f + "' style='width:120px;' /><BR>" + tb.get_file_name(f)
      html += "</TD>"
    html += "</TR></TABLE>"
    html += "</TD>"
    html += "</TR>"    



  # show history result
  html += "<TR>"
  html += "<TD ALIGN=CENTER>Result</TD>"
  for model_name in models.keys():
    html += "<TD ALIGN=LEFT>"
    html += "<PRE>"
    html += "<B>Accuracy     :</B> " + str(models[model_name]["history"].history["accuracy"][-1])     + "<BR>"
    html += "<B>Loss         :</B> " + str(models[model_name]["history"].history["loss"][-1])         + "<BR>"
    html += "<B>Val_Accuracy :</B> " + str(models[model_name]["history"].history["val_accuracy"][-1]) + "<BR>"
    html += "<B>Val_Loss     :</B> " + str(models[model_name]["history"].history["val_loss"][-1])     + "<BR><BR>"

    html += "<B>Total Time   :</B> " + str(sum(models[model_name]["performance"])) + "<BR>"
    html += "<B>Total Epochs :</B> " + str(len(models[model_name]["performance"])) + "<BR>"

    html += "</PRE><HR>"
    
    result_file = config["output"] + "/" + model_name + "/history.result.jpg"    
    html += "<IMG SRC='" + result_file + "' style='width:1000px;' />"
    html += "</TD>"
  html += "</TR>"


  # show decision boundary
  html += "<TR>"
  html += "<TD ALIGN=CENTER>Decision<BR>Boundary</TD>"
  for model_name in models.keys():
    html += "<TD ALIGN=CENTER>"
    result_file = config["output"] + "/" + model_name + "/decision.boundary.Train.jpg"
    html += "<IMG SRC='" + result_file + "' style='width:1000px;' />"
    html += "</TD>"
  html += "</TR>"
  html += "<TR>"
  html += "<TD ALIGN=CENTER>Decision<BR>Boundary</TD>"
  for model_name in models.keys():
    html += "<TD ALIGN=CENTER>"
    result_file = config["output"] + "/" + model_name + "/decision.boundary.Test.jpg"
    html += "<IMG SRC='" + result_file + "' style='width:1000px;' />"
    html += "</TD>"
  html += "</TR>"

  # show model summary
  html += "<TR>"
  html += "<TD ALIGN=CENTER>Model<BR>Summary</TD>"
  for model_name in models.keys():
    html += "<TD ALIGN=LEFT VALIGN=TOP><PRE>"
    summary_file = config["output"] + "/" + model_name + "/model.summary.txt"
    html += tb.read_file(file_name=summary_file)
    html += "</PRE></TD>"
  html += "</TR>"

  html += "</BODY>"
  html += "</HTML>"
  
  
  
  tb.write_file(file_name=report_file, text=html, mode="w")
  return report_file
  
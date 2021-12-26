import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def confusion_matrix(ytrue,ypred,normal=True,f1=False):
    ytrue = ytrue.reshape(-1) # returns the flattened array regardless of the initial shape
    ypred = ypred.reshape(-1)
    one = sum(ytrue)
    zero = len(ytrue) - one
    err1 = sum(ypred[ytrue==0]) #doubt?
    accu = sum(ypred[ytrue==1]) #doubt?
    cm = np.array([[zero-err1, err1],[one-accu,accu]])
#     if f1:
    if normal:
        cm = (cm.astype("float").T/cm.sum(1)).T #here 1 indicates axis
    if f1:
        r,p = cm[1,1],cm[1,1]/(cm[1,1]+cm[0,1])
        f1 = 2*r*p/(r+p)
        return cm,f1
    else:
        return cm  

def plot_comparison(ypred,ytrue):
	fig,(ax1,ax2) = plt.subplots(1,2,figsize=(10,5))
	ax1.imshow(ytrue, label="Truth",cmap="Greens")
	ax1.set_xlabel("Ground Truth")
	im2 = ax2.imshow(ypred, label="Predicted",cmap="Reds")
	ax2.set_xlabel("Predicted")
	return fig




# class Eval():
#     def __init__(self,ypred,ytrue,threshold=0.5):
#         self.ypred = ypred.reshape(-1)
#         self.ytrue = ytrue.reshape(-1)
#   
#self.threshold = threshold #this is not needed?
#         self.classes = ["Normal","Anomaly"]
        
#     def get_conf_matrix(self,normal=True):
#         self.cm =confusion_matrix(self.ytrue,
#                          self.ypred>self.threshold, normal)  
#         return self.cm


def plot_conf_matrix(cm,prior,ann_size=15,closer=True,saver=None,titler="ConfustionMatrix"):
    classes = ["Normal","Anomaly"] 
    classes = ["0","1"]
    ax = sns.heatmap(cm, annot=True, 
                     annot_kws={"size": ann_size},
                     cmap=plt.cm.Blues,
                     xticklabels=classes,
                     yticklabels=classes)
    plt.xlabel("Predicted")
    plt.ylabel("True Labels")
    plt.title(titler)
    plt.tight_layout()
    if saver!= None:
        plt.savefig(prior+ saver+".png",
                   bbox_inches='tight',
                   pad_inches = 0.2)
    if closer:
        plt.close()
    else:
        plt.show()  


from sklearn.metrics import roc_curve #mean_absolute_error,f1_score not needed?
from sklearn.metrics import roc_auc_score

def plotROC(y,yhat,prior,namer="ROC",saver=None,wa=[0.5,0.25,0.15],ax=0):
    if type(ax)==int: 
        loc =plt
    else:
        
        loc = ax
    ytrue = y.reshape(-1)
    yhat = (yhat).reshape(-1)
    for jj in wa:
        w=jj;fpr,tpr,t = roc_curve(ytrue>w,yhat)
        a = roc_auc_score(ytrue>w,yhat)
        loc.plot(fpr,tpr,linewidth=5,
                 label=f"Weight {w}, Area = {a:.3f}")

    loc.plot([0,1],[0,1],"--k")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    loc.legend()
    plt.title(namer)
    if saver!=None:
        plt.savefig(prior+saver,
                   bbox_inches='tight',
                   pad_inches = 0.2)
#     plt.close()
    return loc
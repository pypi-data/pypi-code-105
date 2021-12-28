import statsmodels.api as sm
from sklearn.model_selection import RepeatedKFold
import itertools
import pandas as pd
import numpy as np
import time


'''
package & modules:
    
    (1)
    * BestSubset()
        - params: x_train, y_train
    

    (2.1)
    * BestModelShort()
        - params: none
    
    (2.1.1)
    * varAIC_
    * AIC_
    * indexAIC_
    
    * varBIC_
    * BIC_
    * indexBIC_
    
    * varadjR2_
    * adjR2_
    * indexadjR2_

    (2.2)
    * BestModel()
        - params: n_splits, n_repeats, random_state
        - default: {n_splits:5,
                    n_repeats:1,
                    random_state:123}
    (2.2.1)
    * feat_()
    * mse_()
    * index_()
'''

class BestSubsetShort:
    
    '''
    BestSubsetShort requires a target dataset to be split 
    into train and test set by independent and dependent variables
    as a preliminary task.
    at the init step, the x and y trainset are to be merged
    and x_feature & response be partitioned.
    '''
    
    def __init__(self, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train
        self.x_feature = x_train.columns.to_list()
        self.response = y_train.columns.to_list()
        self.tr_df = pd.concat([x_train, y_train], axis=1)

        
    '''
    Every possible combination of columns is taken into account.
    Comparing the AIC, BIC, adjR2 of the sets of features without a cross validation.
    '''
    def BestModelShort(self):
    
        tic = time.time()
    
        results = []
    
        for k in range(len(self.x_feature)):
            combo_list = list(i for i in itertools.combinations(self.x_feature, k+1))
            #t = 0
            print("Iteration:", k+1, "out of", len(self.x_feature))
        
            for combo in combo_list:
                results.append(compute(combo, self.x_train, self.y_train))
                #t = t + 1
                #print("process: ", round((t/len(combo_list))*100, 2), "%")
        
        # Wrap everything up in a dataframe
        models = pd.DataFrame(results)
   
        # Choose the model with the lowest AIC, BIC and highest adjR2
        # 1) AIC 
        best_aic = models.loc[models['AIC'].argmin()]
        self.varAIC_ = best_aic[1]
        self.AIC_ = best_aic[2]
        self.indexAIC_ = [indx for indx in range(len(self.x_feature)) if self.x_feature[indx] in best_aic[1]]

        # 2) BIC
        best_bic = models.loc[models['BIC'].argmin()]
        self.varBIC_ = best_bic[1]
        self.BIC_ = best_bic[3]
        self.indexBIC_ = [indx for indx in range(len(self.x_feature)) if self.x_feature[indx] in best_bic[1]]
        
        # 3) adjR2
        best_adjR2 = models.loc[models['adjR2'].argmax()]
        self.varadjR2_ = best_adjR2[1]
        self.adjR2_ = best_adjR2[4]
        self.indexadjR2_ = [indx for indx in range(len(self.x_feature)) if self.x_feature[indx] in best_adjR2[1]]
    
        #best_dic = {"Best AIC":best_aic, "Best BIC":best_bic, "Best adjR2":best_adjR2}
    
        toc = time.time()
        print("Processed", models.shape[0], "in", (toc-tic), "seconds.")
        
    # 1) attributes for AIC set
    def varAIC_(self):
        return self.varAIC_
    def AIC_(self):
        return self.AIC_
    def indexAIC_(self):
        return self.indexAIC_
    
    # 2) attributes for BIC set
    def varBIC_(self):
        return self.varBIC_
    def BIC_(self):
        return self.BIC_
    def indexBIC_(self):
        return self.indexadjR2_
    
    # 3) attributes for adjR2 set
    def varadjR2_(self):
        return self.varadjR2_
    def adjR2_(self):
        return self.adjR2_
    def indexadjR2_(self):
        return self.indexadjR2_


class BestSubset(BestSubsetShort):
    
    '''
    BestSubset requires a target dataset to be split 
    into train and test set by independent and dependent variables
    as a preliminary task.
    at the init step, the x and y trainset are to be merged
    and x_feature & response be partitioned.
    
    Every possible combination of columns is taken into account.
    Comparing the average of the k-fold cross-validated Mean Squared Errors(MSE)
    of the sets of features.
    '''
    
    
    def BestModel(self, n_splits=5, n_repeats=1, random_state=123): 
    
        tic = time.time()
        results = []
        
        for k in range(len(self.x_feature)):
            combo_list = list(i for i in itertools.combinations(self.x_feature, k+1))
            #t = 0
            print("Iteration:", k+1, "out of", len(self.x_feature))
        
            for combo in combo_list:
                results.append(kfoldSubset(combo, self.response, self.tr_df, n_splits, n_repeats, random_state))
                
                
                #t = t + 1
                #print("process: ", round((t/len(combo_list))*100, 2), "%")
        
        # Wrap everything up in a nice dataframe
        models = pd.DataFrame(results)
   
        # Choose the model with the lowest MSE
        best_ = models.loc[models['MSE'].argmin()]
        
        self.best_feat = best_[0]
        self.best_mse = best_[1]
        self.best_index = [indx for indx in range(len(self.x_feature)) if self.x_feature[indx] in self.best_feat]

        
        toc = time.time()
        print("Processed", models.shape[0], "in", (toc-tic), "seconds.")
        
        
    '''
    * feat_: get the best set of features selected by the k-fold CV MSE.
    * mse_: get the MSE of the best model.
    * index_: get the indices of the selected features of the best model.
    '''
    
    def feat_(self):
        return self.best_feat
    
    def mse_(self):
        return self.best_mse
    
    def index_(self):
        return self.best_index

    
def kfoldSubset(x_feature,
                response,
                tr_df,
                n_splits=None, 
                n_repeats=None, 
                random_state=None):
        
    cv_MSE_list = []
    
    # Indices of the selected columns
    x_feat = [xi for xi in range(len(tr_df.columns)) if tr_df.columns[xi] in x_feature]
    y_feat = [yi for yi in range(len(tr_df.columns)) if tr_df.columns[yi] in response]
    
    # k-fold CV 
    kf = RepeatedKFold(n_splits = n_splits, n_repeats = n_repeats, random_state = random_state)
   
    # Folding the trainset and splitting them into train and valid sets
    for train_index, val_index in kf.split(tr_df):
        train_X, val_X = tr_df.iloc[train_index, x_feat], tr_df.iloc[val_index, x_feat] 
        train_y, val_y = tr_df.iloc[train_index, y_feat], tr_df.iloc[val_index, y_feat]
        
        # Calculate MSE for each set of features
        cv_model = sm.OLS(train_y, train_X).fit()
        cv_MSE = ((pd.DataFrame(cv_model.predict(val_X), columns = response).subtract(val_y, axis = 1))**2).mean()
        cv_MSE_list.append(cv_MSE)
    
    # Rounding the Cross-validated MSE to compute the mean MSE by sets of features
    Model_MSE = round(np.average(cv_MSE_list), 3)
    sub_dict = {"model":x_feature, "MSE":Model_MSE}
    
    return sub_dict


def compute(x_features, x_train, y_train):
    
    x_feat = [xi for xi in range(len(x_train.columns)) if x_train.columns[xi] in x_features]
    
    modelResult = sm.OLS(y_train, x_train.iloc[:, x_feat]).fit()
    aic = modelResult.aic
    bic = modelResult.bic
    adjr2 = modelResult.rsquared_adj

    sub_dict = {"model":modelResult, "X_features":x_features, "AIC":aic, "BIC":bic, "adjR2":adjr2}
    
    return sub_dict
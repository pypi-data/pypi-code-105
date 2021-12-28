import statsmodels.api as sm
from sklearn.model_selection import RepeatedKFold
import itertools
import pandas as pd
import numpy as np
import time

'''
package & modules:
    
    (1)
    * ForwardStepwise()
        - params: x_train, y_train

    (2)
    * BestModel()
        - params: n_splits, n_repeats, random_state
        - default: {n_splits:5,
                    n_repeats:1,
                    random_state:123}
    (2.1)
    * feat_()
    * mse_()
    * index_()
'''

class ForwardStepwise:
    
    '''
    ForwardStepwise requires a target dataset to be split 
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
    Every possible combinations of columns comprised by a forward-stepwise method is taken into account.
    Comparing the AIC, BIC, adjR2 of the sets of features without a cross validation.
    '''
    def BestModel(self, n_splits=5, n_repeats=1, random_state=123):
    
    
        tic = time.time()
        results = []
    
        for k in range(1, len(self.x_feature)+1):
            bucket = []
            print("Iteration:", k, "out of", len(self.x_feature))
        
            for combo in itertools.combinations(self.x_feature, k):
                if k == 1:
                    bucket.append(kfoldSubset(combo, self.response, self.tr_df, n_splits, n_repeats, random_state))
                       
                else:
                    if set(minMSE_features).issubset(combo):
                        bucket.append(kfoldSubset(combo, self.response, self.tr_df, n_splits, n_repeats, random_state))
        
            sortedResults = sorted(bucket, key = lambda x:x["MSE"])
            results.append(sortedResults[0])
            minMSE_features = sortedResults[0]['model']
        
       
        
        # Wrap everything up in a nice dataframe
        models = pd.DataFrame(results)
   
        # Choose the model with the lowest MSE
        best_ = models.loc[models['MSE'].argmin()]
        #best_features = best_model["model"]
        
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
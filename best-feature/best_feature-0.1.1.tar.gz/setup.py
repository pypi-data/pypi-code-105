from setuptools import setup

setup(name = 'best_feature', 
      URL = 'https://github.com/hshehjue/My_Functions/blob/main/Model_Selection.ipynb',
      LICENSE = 'MIT',
      version = '0.1.1', 
      description = 'python package containing multiple model selection tools: Best Subset Selection via MSE computed by a k-fold CV, Best Subset Selection via three measurements(AIC, BIC, adjR2), Forward-Stepwise Selection', 
      author = 'SeungHeon Han',
      email = 'seung225@gwu.edu',
      packages = ['best_feature'], 
      zip_safe = False)
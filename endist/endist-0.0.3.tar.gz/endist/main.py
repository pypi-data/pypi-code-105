import pandas as pd
import numpy as np
#import pandapower as pp

class Endist():
    def __init__(self):
        # metadata is dataframe, tsdata is dictionary of dataframes
        #self.connectivity = pp.Net()
        self.smart_meter_data = {"metadata": None, "tsdata": None}
        self.MV_LV_transformer_data = {"metadata": None, "tsdata": None}
        self.HV_MV_transformer_data = {"metadata": None, "tsdata": None} 

    # setter and getter for smart_meter_data, MV_LV_transformer_data, HV_MV_transformer_data
    def get_smart_meter_data(self):
        return self.smart_meter_data
    
    def set_smart_meter_data(self, smart_meter_data):
        self.smart_meter_data = smart_meter_data
    
    def get_MV_LV_transformer_data(self):
        return self.MV_LV_transformer_data

    def set_MV_LV_transformer_data(self, MV_LV_transformer_data):
        self.MV_LV_transformer_data = MV_LV_transformer_data

    def get_HV_MV_transformer_data(self):
        return self.HV_MV_transformer_data
    
    def set_HV_MV_transformer_data(self, HV_MV_transformer_data):
        self.HV_MV_transformer_data = HV_MV_transformer_data
    
    # def get_connectivity(self):
    #     return self.connectivity
    
    # def set_connectivity(self, pandapower_network):
    #     self.connectivity = pandapower_network

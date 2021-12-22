import pandas as pd
import numpy as np
import joblib

from mlxtend.preprocessing import TransactionEncoder 

from mba import connection
from mba.config.core import DATASET_DIR, config
from mba.data.data_management import DataFlow

class Feature(object):
    def __init__(self):
        self.df_clean = pd.read_sql_table(table_name=config.data_config.association_table, con=connection)

    def _transactions_to_list(self, persist=True):
        invoice_item_list = []
        for num in list(set(self.df_clean.Invoice.tolist())):
            tmp_df = self.df_clean[self.df_clean['Invoice'] == num]
            tmp_items = tmp_df.Description.tolist()
            invoice_item_list.append(tmp_items)
        if persist:
            joblib.dump(invoice_item_list, f'{DATASET_DIR}/processed/invoice_item_list.pkl')
        return invoice_item_list

    def _recalculate(self):
        invoice_item_list = self._transactions_to_list()
        return invoice_item_list

    def __prepare_data(self, recalculate):
        if recalculate:
            invoice_item_list = self._recalculate()
        else:
            invoice_item_list = DataFlow().read_processed_data_pkl('invoice_item_list.pkl')
        return invoice_item_list

    def _prepare_data(self, recalculate):
        invoice_item_list = self.__prepare_data(recalculate)
        online_encoder = TransactionEncoder()
        online_encoder_array = online_encoder.fit_transform(invoice_item_list)
        online_encoder_df = pd.DataFrame(online_encoder_array, columns=online_encoder.columns_)
        return online_encoder_df
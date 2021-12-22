import pandas as pd
import numpy as np

from mba import connection
from mba.config.core import config
# from mba.data.data_management import DataFlow


class CartFeatures(object):
    def __init__(self):
        self.df_cart = pd.read_sql_table(table_name=config.data_config.transaction_table, con=connection)
        self.df_merged = pd.read_sql_table(table_name=config.data_config.merged_table, con=connection)

    def get_dow_features(self):
        dow_freq = self.df_cart[
            config.data_config.day_of_week].value_counts()
        dow_freq = dict(dow_freq)

        dow = list(dow_freq.keys())
        dow_count = list(dow_freq.values())
        return dow, dow_count

    def get_hod_features(self):
        hod_freq = self.df_cart[config.data_config.hour_of_day].value_counts(
        )
        hod_freq = dict(hod_freq)

        hod = list(hod_freq.keys())
        hod_count = list(hod_freq.values())
        return hod, hod_count

    def get_time_distribution(self):
        groupby_list = [config.data_config.day_of_week,
                        config.data_config.hour_of_day]
        pivot_dict = [config.data_config.day_of_week, config.data_config.hour_of_day,
                      config.data_config.transaction_id_column_name]
        weekday_df = self.df_cart.groupby(
            groupby_list)[config.data_config.transaction_id_column_name].aggregate('count').reset_index()
        weekday_df = weekday_df.pivot(
            *pivot_dict)
        return weekday_df

    def get_number_of_carts_count(self):
        order_group = self.df_cart.groupby(
            config.data_config.user_id_column_name)
        on_count = order_group[config.data_config.order_number_for_user].aggregate(np.max)
        on_count = dict(on_count.value_counts())
        max_baskets = list(on_count.keys())
        max_basket_count = list(on_count.values())
        return max_baskets, max_basket_count

    def get_products_per_department(self):
        departments = self.df_merged[config.data_config.department_name_column].value_counts()
        departments = dict(departments)
        return departments    

    def get_products_per_aisle(self):
        aisles = self.df_merged[config.data_config.aisle_name_column].value_counts()
        aisles = dict(aisles)
        return aisles

    def get_top_products_sold(self):
        products = self.df_merged[config.data_config.product_name_column].value_counts()
        products = dict(products)
        # product = list(products.keys())
        # frequency = list(products.values())
        return products

# TODO: change 'add_to_cart_order' with config
    def get_number_products_in_cart(self):
        orderid_grp = self.df_merged.groupby(config.data_config.transaction_id_column_name)['add_to_cart_order'].aggregate('max').reset_index()
        add_cart = orderid_grp['add_to_cart_order'].value_counts()
        add_cart = dict(add_cart)
        return add_cart


class InventoryFeatures(object):
    def __init__(self) -> None:
        super().__init__()
        self.df_product = pd.read_sql_table(table_name=config.data_config.product_table, con=connection)
        self.df_department = pd.read_sql_table(table_name=config.data_config.department_table, con=connection)
        self.df_aisle = pd.read_sql_table(table_name=config.data_config.aisle_table, con=connection)

    def get_department_distribution(self):
        df = self.df_product.groupby(
            config.data_config.department_id_column).size().reset_index(name='count')
        df_product_department = pd.merge(left=df, right=self.df_department,
                             how='inner', on=config.data_config.department_id_column)
        return df_product_department

    def get_aisle_distribution(self):
        df = self.df_product.groupby(
            config.data_config.aisle_id_column).size().reset_index(name='count')
        df_product_aisle = pd.merge(left=df, right=self.df_aisle,
                             how='inner', on=config.data_config.aisle_id_column)
        return df_product_aisle
    
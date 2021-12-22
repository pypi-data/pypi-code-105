import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go

from mba.config.core import config
from mba.processing.plot_features import InventoryFeatures


class Storage(object):
    def __init__(self):
        inverntoryfeatures = InventoryFeatures()
        self.df_department_distribution = inverntoryfeatures.get_department_distribution()
        self.df_aisle_distribution = inverntoryfeatures.get_aisle_distribution()

    def department_distribution_pie(self, show=False):

        data = go.Pie(labels=self.df_department_distribution[config.data_config.department_name_column],
                      values=self.df_department_distribution['count'])

        fig = go.Figure(data=data)
        if show:
            fig.show()

        return fig

    def aisle_distribution_pie(self, begin=0, end=20, show=False):

        data = go.Pie(labels=self.df_aisle_distribution[config.data_config.aisle_name_column]
                      [begin:end], values=self.df_aisle_distribution['count'][begin:end])

        fig = go.Figure(data=data)
        if show:
            fig.show()

        return fig

    def department_distribution_bar(self, show=False):
        data = go.Bar(y=self.df_department_distribution[config.data_config.department_name_column], x=self.df_department_distribution['count'], orientation='h',
                      marker_color='RoyalBlue',
                      text=self.df_department_distribution['count'])

        fig = go.Figure(data=data)
        if show:
            fig.show()

        return fig

    def aisle_distribution_bar(self, begin=0, end=20, show=False):

        data = go.Bar(y=self.df_aisle_distribution[config.data_config.aisle_name_column][begin:end], x=self.df_aisle_distribution['count'][begin:end], orientation='h',
                      marker_color='RoyalBlue',
                      text=self.df_aisle_distribution['count'][begin:end])

        fig = go.Figure(data=data)
        if show:
            fig.show()

        return fig

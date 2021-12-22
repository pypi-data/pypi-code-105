import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go

from mba.config.core import config
from mba.processing.plot_features import CartFeatures, InventoryFeatures


class Cart(object):
    def __init__(self):
        plot_features = CartFeatures()
        self.dow, self.dow_count = plot_features.get_dow_features()
        self.hod, self.hod_count = plot_features.get_hod_features()
        self.weekday_df = plot_features.get_time_distribution()
        self.max_baskets, self.max_basket_count = plot_features.get_number_of_carts_count()

    def carts_per_day(self, show=False) -> plotly.graph_objs.Figure:
        """number of carts per day graph plot"""

        data = go.Bar(x=self.dow,
                      y=self.dow_count,
                      name='Cart Count by Day of Week',
                      #   marker_color=self.dow,
                      text=self.dow_count,
                      textposition='outside')

        layout = go.Layout(title="Carts per day",
                           title_x=0.5,
                           xaxis=dict(title_text='Day of Week',
                                      showgrid=False),
                           yaxis=dict(title_text='Count', showgrid=False))

        fig = go.Figure(data=data, layout=layout)
        if show:
            fig.show()

        return fig

    def carts_per_hour(self, show=False) -> plotly.graph_objs.Figure:
        """number of carts per hour graph plot"""

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=self.hod,
            y=self.hod_count,
            name='Cart Count by Hour of the Day',
            marker_color='RoyalBlue',
            text=self.hod_count)
        )

        if show:
            fig.show()
        return fig

    def number_of_carts_count(self, show=False) ->plotly.graph_objs.Figure:
        data = go.Bar(
            x=self.max_baskets,
            y=self.max_basket_count,
            name='Maximum Cart Count',
            marker_color='RoyalBlue',
            text=self.max_basket_count)

        layout = go.Layout(title="Maximum Cart Count per Customer",
                           title_x=0.5,
                           xaxis=dict(title_text='Maximum Cart Count',
                                      showgrid=False),
                           yaxis=dict(title_text='Count', showgrid=False))

        fig = go.Figure(data=data, layout=layout)
        if show:
            fig.show()
        return fig

    def time_distribution(self, show=False) -> plotly.graph_objs.Figure:
        """plot number of carts vs days vs hours

        Args:
            show (bool, optional): to show the figure . Defaults to False.

        Returns:
            plotly.graph_objs.Figure: figure
        """

        data = go.Heatmap(
            x=self.weekday_df.index.tolist(),
            y=self.weekday_df.columns.tolist(),
            z=self.weekday_df.values.tolist(),
            colorscale='blues',
        )

        fig = go.Figure(data=data)
        fig.update_layout(width=1000, height=1200)
        fig.update_yaxes(autorange='reversed')

        if show:
            fig.show()
        return fig


class Inventory(object):
    def __init__(self,):
        plot_features = CartFeatures()
        self.departments = plot_features.get_products_per_department() 
        self.aisles = plot_features.get_products_per_aisle()
        self.products = plot_features.get_top_products_sold()
        self.add_cart = plot_features.get_number_products_in_cart()

    def products_per_department(self, show=False) -> plotly.graph_objs.Figure:

        data = go.Bar(
            y=list(self.departments.keys()),
            x=list(self.departments.values()),
            orientation='h',
            name='Departments by Products Sold',
            marker_color='RoyalBlue',
            text=list(self.departments.values()))

        fig = go.Figure(data=data)
        if show:
            fig.show()

        return fig

    def products_per_department_pie(self, show=False) -> plotly.graph_objs.Figure:

        data = go.Pie(
            labels=list(self.departments.keys()),
            values=list(self.departments.values()),
            name='Departments by Products Sold',
        )
        fig = go.Figure(data=data)
        if show:
            fig.show()

        return fig

    def products_per_aisle(self, show=False) -> plotly.graph_objs.Figure:
        

        data = go.Bar(
            y=list(self.aisles.keys()),
            x=list(self.aisles.values()),
            orientation='h',
            marker_color='RoyalBlue',
            text=list(self.aisles.values()))
        fig = go.Figure(data=data)
        if show:
            fig.show()

        return fig

    def products_per_aisle_pie(self, show=False, top=20) -> plotly.graph_objs.Figure:

        data = go.Pie(labels=list(self.aisles.keys())[
                      :top], values=list(self.aisles.values())[:top])
        fig = go.Figure(data=data)
        if show:
            fig.show()

        return fig

    def top_products_sold(self, begin=0, end=20, show=False):
        product = list(self.products.keys())
        frequency = list(self.products.values())


        data = go.Bar(
            y= product[begin:end],
            x= frequency[begin:end],
            orientation='h',
            name=f'Top {end} Products by Frequency',
            marker_color='RoyalBlue',
            text=frequency[begin:end])
        fig = go.Figure(data=data)
        if show:
            fig.show()

        return fig

    def number_products_in_cart(self, show=False):

        data = go.Bar(
            x= list(self.add_cart.keys()),
            y= list(self.add_cart.values()),
            name='Maximum Order Count',
            marker_color='RoyalBlue')
        fig = go.Figure(data=data)
        if show:
            fig.show()

        return fig
                    
                    

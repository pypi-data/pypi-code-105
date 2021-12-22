import os, requests
from pydruid.client import *
from pydruid.utils.aggregators import * 
from pydruid.utils.postaggregator import * 


class HydroDruid:
    def __init__(self, druid_broker_endpoint, druid_broker_port):
        self.druid_broker_endpoint = druid_broker_endpoint
        self.druid_broker_port = druid_broker_port
        self.druid = self.druid_client()
        self.druid_status = self.druid_status()

    def druid_client(self):
        client = PyDruid('http://' + self.druid_broker_endpoint + ':' + self.druid_broker_port, 'druid/v2')
        return client

    def druid_status(self): 
        url = "http://" + self.druid_broker_endpoint + ":" + self.druid_broker_port + "/status/health" 
        response = requests.get(url) 
        if response.status_code == 200 and response.json():
            self.druid_status = True
            return True
        self.druid_status = False
        return False

    def druid_data_sources(self): 
        url = "http://" + self.druid_broker_endpoint + ":" + self.druid_broker_port + "/druid/v2/datasources" 
        response = requests.get(url) 
        return response.json()
    # def druid_timeseries_query():

    def druid_data_source_dimensions(self, druid_datasource_name): 
        url = "http://" + self.druid_broker_endpoint + ":" + self.druid_broker_port + "/druid/v2/datasources/{}".format(druid_datasource_name) 
        response = requests.get(url) 
        return response.json()

    def druid_time_series_query(self, datasource, granularity=None, intervals=None, aggregations=None, post_aggregations=None, filter=None):  
        ts = self.druid.timeseries(
            datasource=datasource,
            granularity=granularity,
            intervals=intervals,
            aggregations=aggregations,
            post_aggregations=post_aggregations,
            filter=filter
        )
        df = self.druid.export_pandas()

        # CLEAN UP DF
        # if granularity == "day":
        #     df['timestamp'] = df['timestamp'].map(lambda x: x.split('T')[0])
        # else:
        #     print("DO SOMETHING WITH TIME AND TZ")
        return df



    def druid_group_by_query(self, datasource, granularity=None, intervals=None, aggregations=None, post_aggregations=None, filter=None, limit_spec=None):  
        ts = self.druid.groupby(
            datasource=datasource,
            granularity=granularity,
            intervals=intervals,
            aggregations=aggregations,
            post_aggregations=post_aggregations,
            filter=filter,
            limit_spec = limit_spec
        )
        df = self.druid.export_pandas()
        # CLEAN UP DF
        # if granularity == "day":
        #     df['timestamp'] = df['timestamp'].map(lambda x: x.split('T')[0])
        # else:
        #     print("DO SOMETHING WITH TIME AND TZ")
        return df
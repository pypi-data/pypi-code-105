import pandas as pd
import numpy as np
import copy
from tqdm import tqdm
from collections import OrderedDict
from .utils import (
    clean_ts,
    p_success,
    p_fail,
    p_warning,
)
import plotly.express as px
import matplotlib.pyplot as plt


def get_ptype(archive_type, proxy_type):
    ptype_dict = {
        ('tree', 'delta Density'): 'tree.MXD',
        ('tree', 'MXD'): 'tree.MXD',
        ('tree', 'TRW'): 'tree.TRW',
        ('tree', 'ENSO'): 'tree.ENSO',
        ('coral', 'Sr/Ca'): 'coral.SrCa',
        ('coral', 'Coral Sr/Ca'): 'coral.SrCa',
        ('coral', 'd18O'): 'coral.d18O',
        ('coral', 'calcification'): 'coral.calc',
        ('coral', 'calcification rate'): 'coral.calc',
        ('sclerosponge', 'd18O'): 'coral.d18O',
        ('sclerosponge', 'Sr/Ca'): 'coral.SrCa',
        ('glacier ice', 'melt'): 'ice.melt',
        ('glacier ice', 'd18O'): 'ice.d18O',
        ('glacier ice', 'dD'): 'ice.dD',
        ('speleothem', 'd18O'): 'speleothem.d18O',
        ('marine sediment', 'TEX86'): 'marine.TEX86',
        ('marine sediment', 'foram Mg/Ca'): 'marine.MgCa',
        ('marine sediment', 'd18O'): 'marine.d18O',
        ('marine sediment', 'dynocist MAT'): 'marine.MAT',
        ('marine sediment', 'alkenone'): 'marine.alkenone',
        ('marine sediment', 'planktonic foraminifera'): 'marine.foram',
        ('marine sediment', 'foraminifera'): 'marine.foram',
        ('marine sediment', 'foram d18O'): 'marine.foram',
        ('marine sediment', 'diatom'): 'marine.diatom',
        ('lake sediment', 'varve thickness'): 'lake.varve_thickness',
        ('lake sediment', 'varve property'): 'lake.varve_property',
        ('lake sediment', 'sed accumulation'): 'lake.accumulation',
        ('lake sediment', 'chironomid'): 'lake.chironomid',
        ('lake sediment', 'midge'): 'lake.midge',
        ('lake sediment', 'TEX86'): 'lake.TEX86',
        ('lake sediment', 'BSi'): 'lake.BSi',
        ('lake sediment', 'chrysophyte'): 'lake.chrysophyte',
        ('lake sediment', 'reflectance'): 'lake.reflectance',
        ('lake sediment', 'pollen'): 'lake.pollen',
        ('lake sediment', 'alkenone'): 'lake.alkenone',
        ('borehole', 'borehole'): 'borehole',
        ('hybrid', 'hybrid'): 'hybrid',
        ('bivalve', 'd18O'): 'bivalve.d18O',
        ('documents', 'Documentary'): 'documents',
        ('documents', 'historic'): 'documents',
    }

    return ptype_dict[(archive_type, proxy_type)]

class ProxyRecord:
    def __init__(self, pid, time, value, lat=None, lon=None, ptype=None,
        value_name=None, value_unit=None, time_name=None, time_unit=None):
        '''
        Parameters
        ----------
        pid : str
            the unique proxy ID

        lat : float
            latitude

        lon : float
            longitude

        time : np.array
            time axis in unit of year CE 

        value : np.array
            proxy value axis

        ptype : str
            the label of proxy type according to archive and proxy information;
            some examples:
            - 'tree.trw' : TRW
            - 'tree.mxd' : MXD
            - 'coral.d18O' : Coral d18O isotopes
            - 'coral.SrCa' : Coral Sr/Ca ratios
            - 'ice.d18O' : Ice d18O isotopes
        '''
        self.pid = pid
        self.time = time
        self.value = value
        self.lat = lat
        self.lon = lon
        self.ptype = ptype
        self.value_name = 'Proxy Value' if value_name is None else value_name
        self.value_unit = value_unit
        self.time_name = 'Time' if time_name is None else time_name
        self.time_unit = 'yr' if time_unit is None else time_unit

    def __add__(self, records):
        ''' Add a list of records into a database
        '''
        newdb = ProxyDatabase()
        newdb.records[self.pid] = self.copy()
        if isinstance(records, ProxyRecord):
            # if only one record
            records = [records]

        if isinstance(records, ProxyDatabase):
            # if a database
            records = [records.records[pid] for pid in records.records.keys()]

        for record in records:
            newdb.records[record.pid] = record

        newdb.refresh()
        return newdb

    def copy(self):
        return copy.deepcopy(self)

    def plotly(self, mute=False, **kwargs):
        time_lb = f'{self.time_name} [{self.time_unit}]'
        value_lb = f'{self.value_name} [{self.value_unit}]'

        _kwargs = {'markers': 'o'}
        _kwargs.update(kwargs)
        fig = px.line(
            x=self.time, y=self.value,
            labels={'x': time_lb, 'y': value_lb},
            **_kwargs,
        )

        if not mute:
            fig.show()

        return fig

    def plot(self, mute=False, figsize=[10, 4], legend=True, **kwargs):
        time_lb = f'{self.time_name} [{self.time_unit}]'
        value_lb = f'{self.value_name} [{self.value_unit}]'

        fig, ax = plt.subplots(figsize=figsize)
        _kwargs = {'marker': 'o'}
        _kwargs.update(kwargs)
        ax.plot(self.time, self.value, label=self.pid, **_kwargs)
        ax.set_xlabel(time_lb)
        ax.set_ylabel(value_lb)
        if legend:
            ax.legend()

        if not mute:
            plt.show()

        return fig, ax



class ProxyDatabase:
    def __init__(self, records=None, source=None):
        '''
        Parameters
        ----------
        records : dict
            a dict of the ProxyRecord objects with proxy ID as keys

        source : str
            a path to the original source file

        '''
        records = {} if records is None else records
        self.records = records
        self.source = source
        if records is not None:
            self.refresh()

    def copy(self):
        return copy.deepcopy(self)

    def refresh(self):
        self.nrec = len(self.records)
        self.pids = [pobj.pid for pid, pobj in self.records.items()]
        self.lats = [pobj.lat for pid, pobj in self.records.items()]
        self.lons = [pobj.lon for pid, pobj in self.records.items()]
        self.type_list = [pobj.ptype for pid, pobj in self.records.items()]
        self.type_dict = {}
        for t in self.type_list:
            if t not in self.type_dict:
                self.type_dict[t] = 1
            else:
                self.type_dict[t] += 1

    def load_df(self, df, pid_column='paleoData_pages2kID', lat_column='geo_meanLat', lon_column='geo_meanLon',
                time_column='year', value_column='paleoData_values', proxy_type_column='paleoData_proxy', archive_type_column='archiveType',
                value_name_column='paleoData_variableName', value_unit_column='paleoData_units',
                verbose=False):
        ''' Load database from a Pandas DataFrame

        Parameters
        ----------
        df : Pandas DataFrame
            a Pandas DataFrame include at least lat, lon, time, value, proxy_type
        
        ptype_psm : dict
            a mapping from ptype to psm
        '''
        if not isinstance(df, pd.DataFrame):
            err_msg = 'the input df should be a Pandas DataFrame.'
            if verbose:
                p_fail(f'ProxyDatabase.load_df() >>> {err_msg}')
            raise TypeError(err_msg)

        records = OrderedDict()

        for idx, row in df.iterrows():
            proxy_type = row[proxy_type_column]
            archive_type = row[archive_type_column]
            ptype = get_ptype(archive_type, proxy_type)
            pid = row[pid_column]
            lat = row[lat_column]
            lon = np.mod(row[lon_column], 360)
            time = np.array(row[time_column])
            value = np.array(row[value_column])
            time, value = clean_ts(time, value)
            value_name=row[value_name_column] if value_name_column in row else None
            value_unit=row[value_unit_column] if value_name_column in row else None

            record = ProxyRecord(
                pid=pid, lat=lat, lon=lon,
                time=time, value=value, ptype=ptype,
                value_name=value_name, value_unit=value_unit,
            )
            records[pid] = record

        # update the attributes
        self.records = records
        self.refresh()

    def __add__(self, records):
        ''' Add a list of records into the database
        '''
        newdb = self.copy()
        if isinstance(records, ProxyRecord):
            # if only one record
            records = [records]

        if isinstance(records, ProxyDatabase):
            # if a database
            records = [records.records[pid] for pid in records.records.keys()]

        for record in records:
            newdb.records[record.pid] = record

        newdb.refresh()
        return newdb

    def __sub__(self, records):
        ''' Subtract a list of records from a database
        '''
        newdb = self.copy()
        if isinstance(records, ProxyRecord):
            # if only one record
            records = [records]

        if isinstance(records, ProxyDatabase):
            # if a database
            records = [records.records[pid] for pid in records.records.keys()]

        for record in records:
            try:
                del newdb.records[record.pid]
            except:
                p_warning(f'Warning: Subtracting {record.pid} faild.')

        newdb.refresh()
        return newdb
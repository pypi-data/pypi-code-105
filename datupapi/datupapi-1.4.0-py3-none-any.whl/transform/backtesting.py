import boto3
import numpy as np
import os
import pandas as pd

from datupapi.configure.config import Config
from datupapi.extract.io import IO
from datupapi.evaluate.errors import Errors

class Backtesting(Config):

    #DOCKER_CONFIG_PATH = 'config.yml'
    DOCKER_CONFIG_PATH = os.path.join('/opt/ml/processing/input', 'config.yml')
    io = IO(config_file=DOCKER_CONFIG_PATH, logfile='data_extraction', log_path='output/logs')
    frr = Errors(config_file=DOCKER_CONFIG_PATH, logfile='data_evaluation', log_path='output/logs')

    def __init__(self, config_file, logfile, log_path, *args, **kwargs):
        Config.__init__(self, config_file=config_file, logfile=logfile)
        self.log_path = log_path


    def format_backtests_export(self, df_backtests):
        """
        Return a dataframe including all backtests partitions generated by create_predictor_backtest_export API's calling

        :param df_backtests: Dataframe with all contatenated backtests
        :return df_backtests: Dataframe concatenating all backtests estimates

        >>> df = format_backtests_export(df_backtests)
        >>> df =
                        var1    var2    var3
                idx0     1       2       3
        """
        try:
            for col in ['timestamp', 'backtestwindow_start_time', 'backtestwindow_end_time']:
                df_backtests[col] = pd.to_datetime(df_backtests[col], format='%Y-%m-%d')
            df_backtests = df_backtests.rename(columns={'item_id': 'Item',
                                                        'timestamp': 'Date',
                                                        'location': 'Location',
                                                        'target_value': 'Target',
                                                        'p5': 'ForecastLo95',
                                                        'p20': 'ForecastLo80',
                                                        'p40': 'ForecastLo60',
                                                        'p50': 'ForecastPoint',
                                                        'p60': 'ForecastUp60',
                                                        'p80': 'ForecastUp80',
                                                        'p95': 'ForecastUp95'
                                                        }
                                               )
            if self.use_location:
                not_forecast_cols = ['backtestwindow_start_time', 'backtestwindow_end_time', 'Item', 'Date', 'Location', 'Target']
            else:
                not_forecast_cols = ['backtestwindow_start_time', 'backtestwindow_end_time', 'Item', 'Date', 'Target']
            forecast_cols = [col for col in df_backtests.columns if all(subcol not in col for subcol in not_forecast_cols)]
            df_backtests[forecast_cols] = df_backtests[forecast_cols].applymap(lambda x: 0 if x < 0 else x)\
                                                                     .applymap(lambda x: round(x))
        except KeyError as err:
            self.logger.exception(f'Invalid column name. Please check dataframe metadata: {err}')
            raise
        return df_backtests


    def create_backtest_dataset(self, df_backtests, backtest_name=None):
        """
        Return a dataframe containing the dates, items and backtesting forecasts for a specific backtest

        :param df_backtests: Dataframe including backtests partitions concatenated
        :param backtest_name: Backtests name to distinguish oldest to newest backtest dataset. Choose from options in config.yml
        :return df_back: Dataframe including dates, items and back forecasts for the specified period

        >>> df = create_backtest_dataset(df_backtests, backtest_name='alpha')
        >>> df =
                        var1    var2    var3
                idx0     1       2       3
        """
        date_ix = 0
        num_backtests = self.backtests
        if backtest_name == self.backtest_ids[0]:
            date_ix = num_backtests - 1
        elif backtest_name == self.backtest_ids[1]:
            date_ix = num_backtests - 2
        elif backtest_name == self.backtest_ids[2]:
            date_ix = num_backtests - 3
        elif backtest_name == self.backtest_ids[3]:
            date_ix = num_backtests - 4
        elif backtest_name == self.backtest_ids[4]:
            date_ix = num_backtests - 5
        else:
            self.logger.exception(f'No valid backtest name. Choose from config.yml options')

        try:
            mask_start = df_backtests['backtestwindow_start_time'] == pd.to_datetime(np.sort(df_backtests['backtestwindow_start_time'].unique())[date_ix])
            mask_end = df_backtests['backtestwindow_end_time'] == pd.to_datetime(np.sort(df_backtests['backtestwindow_end_time'].unique())[date_ix])
            df_back = df_backtests[(mask_start) & (mask_end)].drop(['backtestwindow_start_time', 'backtestwindow_end_time'], axis='columns')
            df_back = df_back.sort_values(['Date'], ascending=False)
            df_back['Week'] = df_back['Date'].dt.isocalendar()['week']
        except KeyError as err:
            self.logger.exception(f'Invalid column name. Please check dataframe metadata: {err}')
            raise
        return df_back


    def compute_bias(self, df_back):
        """
        Return a dataframe including the bias between target value and each forecast interval

        :param df_back: Original backtest dataframe
        :return df_back: Backtest dataframe including bias column for each forecast interval

        >>> df = compute_bias(df)
        >>> df =
                        var1    var2    var3
                idx0     1       2       3
        """
        try:
            intervals_dict = {'0.05': 'Lo95',
                              '0.2': 'Lo80',
                              '0.4': 'Lo60',
                              '0.5': 'Point',
                              '0.6': 'Up60',
                              '0.8': 'Up80',
                              '0.95': 'Up95'
                              }
            intervals_list = [intervals_dict.get(e) for e in self.forecast_types]
            for bias in intervals_list:
                try: 
                    df_back['Bias' + bias] =  abs(df_back['Target'] - df_back['Forecast' + bias])
                except:
                    print("No column found")
        except KeyError as err:
            self.logger.exception(f'Invalid column name. Please check dataframe metadata: {err}')
            raise
        return df_back


    def compute_tracking_bias(self, df_back):
        """
        Return a dataframe including the tracking bias for each date

        :param df_back: Original backtest dataframe
        :return df_back: Backtest dataframe including tracking bias column for each date

        >>> df = compute_tracking_bias(df)
        >>> df =
                        var1    var2    var3
                idx0     1       2       3
        """
        try:
            intervals_dict = {'0.05': 'Lo95',
                              '0.2': 'Lo80',
                              '0.4': 'Lo60',
                              '0.5': 'Point',
                              '0.6': 'Up60',
                              '0.8': 'Up80',
                              '0.95': 'Up95'
                              }
            bias_cols = ['Bias' + intervals_dict.get(e) for e in self.forecast_types]
            
            df_back['TrackingBias'] = df_back[df_back.columns.intersection(bias_cols)].idxmin(axis='columns')\
                                                         .str.strip('Bias')
        except KeyError as err:
            self.logger.exception(f'Invalid column name. Please check dataframe metadata: {err}')
            raise
        return df_back


    def compute_tracked_bias(self, df_back):
        """
        Return a dataframe including the tracked bias for each item

        :param df_back: Original backtest dataframe
        :return df_back: Backtest dataframe including tracking bias column for each item

        >>> df = compute_tracked_bias(df)
        >>> df =
                        var1    var2    var3
                idx0     1       2       3
        """
        try:
            for item in df_back['Item'].unique():
                mask = df_back['Item'] == item
                df_back.loc[mask, 'SuggestedInterval'] = df_back.loc[mask, 'TrackingBias']\
                                                                .value_counts()\
                                                                .index[0]
        except KeyError as err:
            self.logger.exception(f'Invalid column name. Please check dataframe metadata: {err}')
            raise
        return df_back


    def compute_tracked_bias_forecast(self, df_back):
        """
        Return a dataframe including the tracked bias forecast for each item and date

        :param df_back: Original backtest dataframe
        :return df_back: Backtest dataframe including tracking bias column for each item and date

        >>> df = compute_tracked_bias_forecast(df)
        >>> df =
                        var1    var2    var3
                idx0     1       2       3
        """
        try:
            tracked_bias_forescast = []
            for row_ix, row in df_back.iterrows():
                tracked_bias_forescast.append(row['Forecast' + row['SuggestedInterval']])
            df_back['SuggestedForecast'] = tracked_bias_forescast
        except KeyError as err:
            self.logger.exception(f'Invalid column name. Please check dataframe metadata: {err}')
            raise
        return df_back


    def compute_tracked_bias_error(self, df_back, error_types=['WMAPE', 'MASE']):
        """
        Return a dataframe including the specified forecast error between target and tracked bias forecast

        :param df_back: Original backtest dataframe
        :param error_types: List of forecast errors to compute among sMAPE, MASE, WMAPE, MAPE, WAPE, RMSE, etc. Default WMAPE.
        :return df_back: Backtest dataframe including tracking bias column for each item and date

        >>> df = compute_tracked_bias_error(df, error_types=['WMAPE', 'MASE', 'sMAPE'])
        >>> df =
                        var1    var2    var3
                idx0     1       2       3
        """
        try:
           for item in df_back['Item'].unique():
            mask = df_back['Item'] == item
            forecast_col = 'Forecast' + df_back[mask]['SuggestedInterval'].values[0]
            target_ts = df_back[mask]['Target'].values
            forecast_ts = df_back[mask][forecast_col].values
            for error_type in error_types:
                if error_type == 'sMAPE':
                    df_back.loc[mask, error_type] = round(self.frr.compute_smape(target_ts, forecast_ts), 2)
                elif error_type == 'WMAPE':
                    df_back.loc[mask, error_type] = round(self.frr.compute_wmape(target_ts, forecast_ts), 2)
                elif error_type == 'MASE':
                    df_back.loc[mask, error_type] = round(self.frr.compute_mase(target_ts, forecast_ts), 2)
                elif error_type == 'WAPE':
                    df_back.loc[mask, error_type] = round(self.frr.compute_wape(target_ts, forecast_ts), 2)
                elif error_type == 'RMSE':
                    df_back.loc[mask, error_type] = round(self.frr.compute_mape(target_ts, forecast_ts), 2)
                elif error_type == 'MAPE':
                    df_back.loc[mask, error_type] = round(self.frr.compute_rmse(target_ts, forecast_ts), 2)
                elif error_type == 'cMAPE':
                    df_back.loc[mask, error_type] = round(self.frr.compute_mape_jet(target_ts, forecast_ts), 2)
                else:
                    self.logger.exception(f'No valid forecast error name. Choose from sMAPE, WMAPE, MASE, WAPE, RMSE')
                df_back = df_back.replace([np.inf, -np.inf], np.nan)
                df_back = df_back.fillna(0)
        except KeyError as err:
            self.logger.exception(f'Invalid column name. Please check dataframe metadata: {err}')
            raise
        return df_back


    def concat_backtest_datasets(self, q_backtest=None, backtests_names=None, datalake_path_=None):
        """
        Return a dataframe including all formatted backtest datasets

        :param q_backtest: Backtesting dataset name stored in the datalake
        :param backtests_names: List of backtests names to concat, e.g. alpha, bravo, etc.
        :param datalake_path_: Datalake path to download the backtest files from. Do not include bucket name
        :return df_backtest: Dataframe including all formatted backtest datasets

        >>> df = concat_backtest_datasets(q_backtest='Qback', backtests_names=['alpha', 'bravo'], datalake_path_='path/to/backtests/folder')
        >>> df =
                        var1    var2    var3
                idx0     1       2       3
        """
        df_backtest = pd.DataFrame()
        try:
            for backtest in backtests_names:
                df_back = self.io.download_csv(q_name=q_backtest + '-' + backtest,
                                               datalake_path=datalake_path_,
                                               )
                df_backtest = pd.concat([df_backtest, df_back], axis='rows').drop_duplicates()
            df_backtest['Date'] = pd.to_datetime(df_backtest['Date'], format='%Y-%m-%d')

        except KeyError as err:
            self.logger.exception(f'Invalid column name. Please check dataframe metadata: {err}')
            raise
        return df_backtest


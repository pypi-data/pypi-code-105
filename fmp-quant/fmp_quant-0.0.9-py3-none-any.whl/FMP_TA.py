import pandas as pd
import numpy as np
import ta

class FMP_TA:
    def __init__(self):
        pass


    def get_volatilty_with_bb(self,df:pd.DataFrame,close:str='close'):

        """ 
        Add Bollinger Bands Trend Indicator to Pandas DataFrame 
        Adding 5 new columns, the SMA 20, two High STDEV 1 & 2, and two Low STDEV 1 & 2

        Parameters:
        -----------
            df pd.DataFrame:
                Pandas DataFrame with HLOC data from the financial instrument to analyze

            with_col str:
                The name of the column where the price is stored, usually close or adjClose

        Returns:
        --------
            pd.DataFrame:
                DataFrame containing the same information given, plus the new columns
        
        """



        stock = df.copy()
        boll_std1 = ta.volatility.BollingerBands(close=stock[close],window=20,window_dev=1)
        boll_std2 = ta.volatility.BollingerBands(close=stock[close],window=20,window_dev=2)

        stock['Bollinger Band High Dev 2'] = boll_std2.bollinger_hband()
        stock['Bollinger Band Low Dev 2'] = boll_std2.bollinger_lband()
        stock['SMA 20'] = boll_std2.bollinger_mavg()

        stock['Bollinger Band High Dev 1'] = boll_std1.bollinger_hband()
        stock['Bollinger Band Low Dev 1'] = boll_std1.bollinger_lband()

        one = stock[close] > stock['Bollinger Band High Dev 2']
        two = stock[close].between(stock['Bollinger Band High Dev 1'], stock['Bollinger Band High Dev 2'])
        three = stock[close].between(stock['SMA 20'],stock['Bollinger Band High Dev 1'])

        four = stock[close].between(stock['Bollinger Band Low Dev 1'], stock['SMA 20'])  
        five = stock[close].between(stock['Bollinger Band Low Dev 2'],stock['Bollinger Band Low Dev 1'])
        six = stock[close] < stock['Bollinger Band Low Dev 2']

        bb_trend_conditions = [one,two,three,four,five,six]  

        bb_trend_values = [3,2,1,-1,-2,-3]

        stock['BB Trend'] = np.select(bb_trend_conditions, bb_trend_values)

        stock['is_uptrend'] = np.where(stock['BB Trend'] > 1,1,0)
        stock['BB Trend %'] = stock['BB Trend'].pct_change()

        return stock


    def get_emas(self,df:pd.DataFrame, emas:[int] = [9,20,50,200],close='close'):
        stock = df.copy()


        for ema in emas:
            stock[f'EMA {ema}'] = ta.trend.ema_indicator(stock[close],ema)
        
        return stock


    #-- PSAR ----------------------------------------------------------------------------------


    def get_PSAR(self,df:pd.DataFrame,high:str='high',low:str='low',close:str='close'):
        
        my_df = df.copy()
        psar_df = ta.trend.PSARIndicator(
            high = my_df[high],
            low = my_df[low],
            close = my_df[close]
        )
        
        my_df['PSAR down'] = psar_df.psar_down()
        my_df['PSAR up'] = psar_df.psar_up()
        
        return my_df

    # -- RSI -----------------------------------------------------------------------------------

    def get_RSI(self,df:pd.DataFrame,close:str = 'close'):
        
        my_df = df.copy()
        
        my_df['RSI'] = ta.momentum.rsi(my_df[close])
        
        return my_df



    def crossing(self,df:pd.DataFrame,
                 price:str,
                 close:str = 'close',
                 open:str = 'open',
                 low:str = 'low',
                 high:str = 'high',
                 direction:str = 'up'):
        
        if direction == 'up':

            return np.where((df[open] < df[price]) & (df[close] > df[price]),1,0)

        elif direction == 'down':

            return np.where((df[open] > df[price]) & (df[close] < df[price]),1,0)

        else:

            raise ValueError(f"{direction} is not available, only up or down")

    def get_strategy_I(self,df:pd.DataFrame, close:str = 'close',
                    high:str = 'high',
                    low:str = 'low',
                    open:str = 'open',
                    volume:str = 'volume') -> pd.DataFrame:
        
        
        ta_df = self.get_volatilty_with_bb(df = df, close = close)
        
        ta_df = self.get_emas(df=ta_df,close=close)
        
        ta_df = self.get_PSAR(df=ta_df,high=high,low=low,close=close)
        
        ta_df = self.get_RSI(df=ta_df,close=close)

        ta_df['Crossing Down EMA 20'] = self.crossing(ta_df,price='EMA 20',direction='down')

        ta_df['Crossing Down EMA 50'] = self.crossing(ta_df,price='EMA 50', direction='down')

        ta_df['Crossing Down EMA 200'] = self.crossing(ta_df,price='EMA 200', direction='down')

        ta_df['Crossing Up EMA 20'] = self.crossing(ta_df,price='EMA 20', direction='up')

        ta_df['Crossing Up EMA 50'] = self.crossing(ta_df,price='EMA 50', direction='up')

        ta_df['Crossing Up EMA 200'] = self.crossing(ta_df,price='EMA 200', direction='up')

        ta_df['Entering Sell Zone'] = self.crossing(ta_df,price='Bollinger Band Low Dev 1',direction='down')

        ta_df['Entering Buy Zone'] = self.crossing(ta_df,price='Bollinger Band High Dev 1',direction='up')
        
        return ta_df
        
    def get_last_action(self,df:pd.DataFrame):

        alert_cols = ['Crossing Down EMA 20','Crossing Down EMA 50', 'Crossing Down EMA 200', 'Crossing Up EMA 20', 'Crossing Up EMA 50', 'Crossing Up EMA 200','Entering Sell Zone', 'Entering Buy Zone']

        most_recent_action = df.tail(1)

        if most_recent_action['Most Recent Action'].values[0] == 1:

            melt_alert = most_recent_action[alert_cols].melt(var_name='Message', value_name='Indicator')

            target_message = melt_alert[melt_alert['Indicator'] == 1].values[0][0]

            alert_time, alert_stock, alert_price = most_recent_action[['symbol', 'close']].reset_index().values.tolist()[0]

            alert_time = alert_time.strftime("%Y-%m-%d, %H:%M:%S")

            return f'{alert_stock}: {target_message} at {alert_time} @ {alert_price}'

        else:
            return None
    
    
    
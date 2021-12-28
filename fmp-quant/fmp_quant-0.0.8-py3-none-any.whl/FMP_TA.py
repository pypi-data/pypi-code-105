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

    def get_strategy_I(self,df:pd.DataFrame, close:str = 'close',
                    high:str = 'high',
                    low:str = 'low',
                    open:str = 'open',
                    volume:str = 'volume') -> pd.DataFrame:
        
        
        ta_df = self.get_volatilty_with_bb(df = df, close = close)
        
        ta_df = self.get_emas(df=ta_df,close=close)
        
        ta_df = self.get_PSAR(df=ta_df,high=high,low=low,close=close)
        
        ta_df = self.get_RSI(df=ta_df,close=close)
        
        return ta_df
        
    
    
    
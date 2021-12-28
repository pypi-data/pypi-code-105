
import requests
import pandas as pd
import numpy as np
import time

class FMP_CONNECTION(object):
    
    def __init__(self,api_key:str):
        self._api_key = api_key
        
    def set_apikey(self,new_apikey):
        self._api_key = new_apikey
    
    def get_apikey(self) -> str:
        return self._api_key
        
    def _get_df(self,url:str,is_historical:bool = False) -> pd.DataFrame:
        
        response = requests.get(url)
        
        if response.status_code == 200:
            
            if response.json() == {}:
                print('Requested instrument is empty when retrieving data')
                return None
            
            if is_historical == False:
                
                response_df = pd.DataFrame.from_dict(response.json())
                
                return response_df
            else:
                symbol = response.json()['symbol']
                
                df = pd.DataFrame.from_dict(response.json()['historical'])
                
                df.insert(0,'symbol',symbol)
                
                df['date'] = pd.to_datetime(df['date'],infer_datetime_format=True)
                
                df.sort_values(by='date',ascending=True,inplace=True)
                
                df.set_index('date',inplace=True)
                
                df.set_index = pd.to_datetime(df.index, infer_datetime_format=True)
                
                return df
        
        else:
            raise ConnectionError('Could not connect to FMP Api, this was the response: \n',response.json())
            
    
    def historical_price_by_interval(self,ticker:str,interval:str='1d') -> pd.DataFrame:

        """
        Retrieve historical price data from various time granularities

        Parameters
        ----------
        ticker:str :
            The ticker of the financial instrument to retrieve historical price data. 

        
        api_key:str :
            your FMP API Key
        
        interval: {1min,5min,15min,30min,1hour,4hour,1d,1w,1m,1q,1y} :
            The granularity of how often the price historical data must be retrieved
             (Default value = '1d')

        Returns
        -------

        pd.DataFrame

        """

        url = None

        # Retrieve Historical info from 1 min to 4 hours

        if interval in ['4hour','1hour','30min','15min','5min','1min']:
            url = f'https://financialmodelingprep.com/api/v3/historical-chart/{interval}/{ticker}?apikey={self._api_key}'

            historical_df = self._get_df(url)
            historical_df.insert(0,'symbol',ticker)

            if 'close' and 'date' in list(historical_df.columns):

            

                historical_df.sort_values(by='date',ascending=True,inplace=True)

                historical_df.set_index('date',inplace=True)

                historical_df.index = pd.to_datetime(historical_df.index, infer_datetime_format=True)

                historical_df['change'] = historical_df['close'].pct_change()            
            

            

            return historical_df

        # Retrieve Daily Info

        elif interval == '1d':

            url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?apikey={self._api_key}'

            historical_df = self._get_df(url,True)

            historical_df['change'] = historical_df['close'].pct_change()

            return historical_df

        url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?apikey={self._api_key}'

        historical_df = self._get_df(url,True)

    

        historical_df['daily'] = pd.to_datetime(historical_df.index, infer_datetime_format=True)

        # Retrieve Weekly, Monthly, Quarterly and Yearly Price Data

        if interval == '1w':
        
            historical_df['week'] = historical_df['daily'].dt.to_period('w').apply(lambda r: r.start_time)

            df = historical_df.drop_duplicates(subset=['week'],keep='first')

            df['change'] = df['close'].pct_change()

            return df

        elif interval == '1m':

            historical_df['monthly'] = historical_df['daily'].astype('datetime64[M]')

            df = historical_df.drop_duplicates(subset=['monthly'],keep='first')

            df['change'] = df['close'].pct_change()

            return df

        elif interval == '1q':

            historical_df['quarter'] = historical_df['daily'].dt.to_period('q')

            df = historical_df.drop_duplicates(subset=['quarter'], keep='first')

            df['change'] = df['close'].pct_change()

            return df

        elif interval == '1y':

            historical_df['year'] = historical_df['daily'].dt.year

            df = historical_df.drop_duplicates(subset=['year'],keep='first')

            df['change'] = df['close'].pct_change()

            return df
    
        else:

            raise ValueError('unsupported interval for ',interval,'check your spelling')
            
            
    def historical_closing_price(self,ticker:str,interval:str = '1d'):
        url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?serietype=line&apikey={self._api_key}'
    
        df = self._get_df(url,True)
    
        if df is None:
            return None
    
        # df['date'] = pd.to_datetime(df.index, infer_datetime_format=True)
    
        if interval == '1d':
            return df

        elif interval == '1w':
            df['week'] = df['date'].dt.to_period('w').apply(lambda r: r.start_time)
            df = df.drop_duplicates(subset=['week'], keep='first')
            df = df.drop(columns=['week'])
                
        elif interval == '1m':
        
            df['monthly'] = df['date'].astype('datetime64[M]')
        
            df = df.drop_duplicates(subset=['monthly'],keep='first')
        
            df = df.drop(columns=['monthly'])
        
            df['date'] = df['date'].astype('datetime64[M]')

        elif interval == '1q':

            df['quarter'] = df['date'].dt.to_period('q')

            df = df.drop_duplicates(subset=['quarter'], keep='first')
        
            df = df.drop(columns=['quarter'])

        elif interval == '1y':

            df['year'] = df['date'].dt.year

            df = df.drop_duplicates(subset=['year'],keep='first')
        
            df = df.drop(columns=['year'])
        
        df = df.drop(columns=['date'])
    
        return df
    
    def get_closing_prices(self,tickers:[str], interval:str = '1d', from_date:str = None):
    
        if isinstance(tickers,str):
        
            df = self.historical_closing_price(tickers,interval)
        
            closing_df = pd.pivot_table(data=df,index=df.index,columns='symbol',values='close',aggfunc='mean')
            closing_df.index = pd.to_datetime(closing_df.index, infer_datetime_format=True)
        
            from_d = from_date if from_date != None else closing_df.index.min()
        
            return closing_df[from_d:]
        else:
        
            dfs = []
    
            for ticker in tickers:
                df = self.historical_closing_price(ticker,interval)
                dfs.append(df)
    
            x = pd.concat(dfs)
    
            closing_df = pd.pivot_table(data=x, index=x.index, columns='symbol',values='close',aggfunc='mean')
            closing_df.index = pd.to_datetime(closing_df.index, infer_datetime_format=True)
    
            from_d = from_date if from_date != None else closing_df.index.min()

            return closing_df[from_d:]


    ## CRYPTO CURRENCIES RELATED

    def get_crypto_quote(self,ticker):

      if isinstance(ticker,str):

        url = f'https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={self.get_apikey()}'

        df = self._get_df(url)

        return df
      elif isinstance(ticker,list):

        dfs = []

        for tick in ticker:
          url = f'https://financialmodelingprep.com/api/v3/quote/{tick}?apikey={self.get_apikey()}'

          df = self._get_df(url)

          dfs.append(df)
        
        cryptos = pd.concat(dfs)
        cryptos.set_index('symbol',inplace=True)

        return cryptos

    def get_available_cryptos(self,min_marketcap=None):
        url = f'https://financialmodelingprep.com/api/v3/symbol/available-cryptocurrencies?apikey={self.get_apikey()}'
    
        df = self._get_df(url)
    
        tickers = df['symbol'].unique()
    
        quotes_info = []
    
        for ticker in tickers:
        
            quote = self.get_crypto_quote(ticker=ticker)
        
            time.sleep(0.1)
        
            quotes_info.append(quote)
        
    
        quotes_df = pd.concat(quotes_info)
        
        merged_df = pd.merge(df, quotes_df, on='symbol',how='left')
    
        merged_df = merged_df[merged_df['marketCap'] > 0]
    
        # Calculate % Off Highs
    
        merged_df["% Off Highs"] = merged_df['price'] / merged_df['yearHigh'] - 1
    
        # Calculate if it is on a Bear Market
    
        merged_df['Is Bear Market'] = np.where(np.abs(merged_df['% Off Highs']) >= 0.20,1,0)
    
        merged_df['Is In Correction'] = np.where(np.abs(merged_df['% Off Highs']).between(0.10,0.20), 1, 0)

        merged_df.rename(columns={
        'name_x':'name'
        },inplace=True)
        
        merged_df.drop(columns='name_y',inplace=True)
    
    
    
        return merged_df


    ## GET FUNDAMENTALS

    def get_financial_statements(self,ticker:str, interval:str = 'annual',type_statement:str='income-statement'):
    
        url = f'https://financialmodelingprep.com/api/v3/{type_statement}/{ticker}?period={interval}&apikey={self.get_apikey()}'
    
        df = self._get_df(url)
    
        df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)
    
        df['ym'] = df['date'].astype('datetime64[M]')
    
        return df

    def get_full_financial_statements(self,ticker:str,interval:str='annual'):
        url = f'https://financialmodelingprep.com/api/v3/financial-statement-full-as-reported/{ticker}?apikey={self.get_apikey()}'
    
        df = self._get_df(url)
    
        df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)
    
        return df

    def get_enterprise_value(self,ticker:str,interval:str='annual'):

        url = f'https://financialmodelingprep.com/api/v3/enterprise-values/{ticker}?&apikey={self.get_apikey()}'
    
        df = self._get_df(url)
    
        df['date'] = pd.to_datetime(df['date'],infer_datetime_format=True)
    
        return df

    def get_insider_trading(self,ticker:str):
        
        url = f'https://financialmodelingprep.com/api/v4/insider-trading?symbol={ticker}&apikey={self.get_apikey()}'

        df = self._get_df(url)

        df['filingDate'] = pd.to_datetime(df['filingDate'], infer_datetime_format=True)

        df['transactionDate'] = pd.to_datetime(df['transactionDate'], infer_datetime_format=True)

        df.set_index('filingDate',inplace=True)

        return df

    def get_filing_dates(self,cik:str):

        url = f'https://financialmodelingprep.com/api/v3/form-thirteen-date/{cik}?apikey={self.get_apikey()}'

        df = self._get_df(url)

        df.columns = ['date']

        return df

    def get_institutional_13f(self,cik:str,date:str):
        url = f'https://financialmodelingprep.com/api/v3/form-thirteen/{cik}?date={date}&apikey={self.get_apikey()}'

        df = self._get_df(url)

        df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)

        df['fillingDate'] = pd.to_datetime(df['fillingDate'], infer_datetime_format=True)

        df.set_index('date',inplace=True)

        return df

    def get_index_tickers(self,index='dowjones'):

        """
        Dow Jones: dowjones
        S&P 500: sp500
        Nasdaq: nasdaq 
        
        """

        url = f'https://financialmodelingprep.com/api/v3/{index}_constituent?apikey={self.get_apikey()}'
        
        df = self._get_df(url)

        return df


    def get_financial_ratios(self,ticker:str,interval='quarter'):
        url = f'https://financialmodelingprep.com/api/v3/ratios/{ticker}?period={interval}&apikey={self.get_apikey()}'

        df = self._get_df(url)

        return df

    def get_key_metrics(self,ticker:str, interval='quarter'):

        url = f'https://financialmodelingprep.com/api/v3/key-metrics/{ticker}?period={interval}&apikey={self.get_apikey()}'

        df = self._get_df(url)

        year_period = df['date'].apply(lambda s: s[:4]).astype(str) + ' ' + df['period']

        df.insert(3,'year_period',year_period)

        df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)

        df.sort_values(by='date',ascending=True,inplace=True)

        df.set_index('year_period',inplace=True)

        return df


    ## GET ECONOMIC INDICATORS

    def get_economic_indicator(self,indicator:str):
    
        url = f'https://financialmodelingprep.com/api/v4/economic?name={indicator}&apikey={self.get_apikey()}'
    
        df = self._get_df(url)
    
        df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)

        df = df.sort_values(by='date',ascending=True)
    
        df.set_index('date',inplace=True)
    
        df.rename(columns={
        'value':indicator
        },inplace=True)
    
        return df

    def get_interest_rates(self,from_date:str,to_date:str):
        url = f'https://financialmodelingprep.com/api/v4/treasury?from={from_date}&to={to_date}&apikey={self.get_apikey()}'

        df = self._get_df(url)

        df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)

        df.set_index('date',inplace=True)

        return df

    def get_available_etfs(self):
        url = f'https://financialmodelingprep.com/api/v3/symbol/available-etfs?apikey={self.get_apikey()}'

        df = self._get_df(url)

        return df

    def get_commitment_report_tickers(self):

        url = f'https://financialmodelingprep.com/api/v4/commitment_of_traders_report/list?apikey={self.get_apikey()}'

        df = self._get_df(url)

        return df

    def get_commitment_report(self,ticker):

        url = f'https://financialmodelingprep.com/api/v4/commitment_of_traders_report_analysis/{ticker}?apikey={self.get_apikey()}'

        df = self._get_df(url)

        df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)

        df.set_index('date',inplace=True)

        return df

    def company_quote(self, ticker):

        if isinstance(ticker,str):

            url = f'https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={self.get_apikey()}'

            df = self._get_df(url)

            df.set_index('symbol',inplace=True)

            return df
        elif isinstance(ticker, list):

            text = ''.join(i + ',' for i in ticker) 

            text = text[:-1]

            url = f'https://financialmodelingprep.com/api/v3/quote/{text}?apikey={self.get_apikey()}'

            df = self._get_df(url)

            df.set_index('symbol',inplace=True)

            return df

        else:
            return None

    
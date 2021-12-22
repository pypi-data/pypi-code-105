from typing import List, Union, Dict
import datetime as dt
import pandas as pd

class InvalidDateTime(BaseException):
    pass

def dict2url(**kwargs):
    arg_str = []
    for k, v in kwargs.items():
        if v and (k != 'token'):
            arg_str.append( f'{k}={v}' )
    if 'token' in kwargs:
        arg_str.append( f"token={kwargs.get('token')}" )
    return '&'.join( arg_str )

def dt2str(datelike):
    if isinstance(datelike, str):
        d = pd.to_datetime(datelike)
    elif not isinstance(datelike, (dt.datetime, dt.date)):
        raise InvalidDateTime(f'{datelike} is neither str nor datelike object')
    return d.strftime('%Y-%m-%d')

def ticker2list(ticker):
    if isinstance(ticker, str):
        return [ticker]
    elif isinstance(ticker, list):
        return ticker

def apply_fmt_vals(fmt, vals=Dict):
    print(fmt)
    return fmt.format(**vals)

def res2df(res, tickers: List[str]):
    if isinstance(res, list) and len(res) > 0:
        if isinstance(res[0], list):
            if tickers is None:
                tickers = [''] * len(res)
                add_symbol = False
            else:
                add_symbol = True
            df = []
            for ticker, ticker_data in zip(tickers, res):
                for item in ticker_data:
                    df_update = pd.json_normalize(item)
                    if add_symbol:
                        df_update.loc[:, 'symbol'] = ticker
                    df.append(df_update)
            return pd.concat(df, axis=0)
        elif isinstance(res[0], dict):
            return pd.json_normalize(res)
    return res
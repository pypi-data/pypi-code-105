from async_mixin import AsyncHttpMixin
from .util import *
## REST Endpoints: https://api.tiingo.com/documentation/end-of-day

BASE_EOD_URL = 'https://api.tiingo.com/tiingo/daily'

META_DATA_URL = '/'.join([f'{BASE_EOD_URL}','{ticker}'])

PRICES_URL = '/'.join([f'{BASE_EOD_URL}','{ticker}','prices'])

NEWS_URL = 'https://api.tiingo.com/tiingo/news'

URL_ARG_FMT = '{url}?{arg_str}'

class Tiingo(AsyncHttpMixin):

    def __init__(self, token: str, rate: int=60, period: int=60):
        super(Tiingo, self).__init__()
        self.token = token
        self.set_rate_limit(n=rate, p=period)

    @property
    def headers(self):
        return {
            'Content-Type': 'application/json'
        }

    def _gen_urls(self, url_fmt: str, vals=List[Dict]):
        return list(map(apply_fmt_vals,
                        [url_fmt] * len(vals),
                        vals
                        )
                    )
    def _append_url_args(self, urls: List[str], **kwargs):
        updated_urls = []
        arg_str = dict2url(**kwargs)
        print(kwargs, arg_str)
        for url in urls:
            updated_urls.append( URL_ARG_FMT.format(url=url,
                                                    arg_str=arg_str)
                                 )
        return updated_urls

    def _get_ticker_urls(self, url_fmt: str, ticker: Union[str, List[str]]):
        if isinstance(ticker, str):
            ticker_list = [dict(ticker=ticker)]
        else:
            ticker_list = [dict(ticker=tick) for tick in ticker]
        return self._gen_urls(url_fmt=url_fmt, vals=ticker_list)

    def meta_data(self, ticker: Union[str, List[str]]):
        ticker_urls = self._get_ticker_urls(META_DATA_URL, ticker)
        ticker_urls = self._append_url_args(ticker_urls,
                                            token=self.token,
        )
        return res2df(
                    self.pipeline(self.process_gets, args=[], kwargs=dict(urls=ticker_urls)),
                    ticker=ticker2list(ticker)
        )

    def last(self, ticker: Union[str, List[str]]):
        ticker_urls = self._get_ticker_urls(PRICES_URL, ticker)
        ticker_urls = self._append_url_args(ticker_urls,
                                            token=self.token,
        )
        return res2df(
                    self.pipeline(self.process_gets, args=[], kwargs=dict(urls=ticker_urls)),
                    ticker=ticker2list(ticker)
        )

    def historical_prices(self,
                          ticker: Union[str, List[str]],
                          start: Union[str, dt.datetime]=None,
                          end: Union[str, dt.datetime]=None,
                          resample_freq: str=None,
                          ):

        if start is None:
            start = dt.datetime.today() - dt.timedelta(365)
        start = dt2str(start)

        if end is not None:
            end = dt2str(end)

        ticker_urls = self._get_ticker_urls(PRICES_URL, ticker)
        ticker_urls = self._append_url_args(ticker_urls,
                                            startDate=start,
                                            endDate=end,
                                            resample_freq=resample_freq,
                                            token=self.token,
        )
        return res2df(
                    self.pipeline(self.process_gets, args=[], kwargs=dict(urls=ticker_urls)),
                    tickers=ticker2list(ticker)
        )

    def news(self, **kwargs):
        news_url = self._append_url_args([NEWS_URL], **kwargs)
        return res2df(
            self.pipeline(self.process_gets, args=[], kwargs=dict(urls=news_url)),
            tickers=None
        )

    def crypto_prices(self, currency_pair: Union[str, List[str]]):
        pass
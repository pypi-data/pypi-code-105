from datetime import datetime


class RandomStr:
    def geTimeStr(self, pre="", strf="%Y%m%d%H%M%S"):
        time_str = datetime.now().strftime(strf)
        return '{}{}'.format(pre, time_str)

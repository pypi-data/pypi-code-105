import datetime
from django import template

from db_hj3415 import mongo
from bokeh_hj3415 import graphs, data

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


register = template.Library()


@register.inclusion_tag('market_graphs/market_graphs.html')
def get_market_graphs():
    mi_db = mongo.MI()

    # mi_db.chg_addr('mongodb://192.168.0.173:27017')

    # Market Index 관련 코드
    recent_mi = {}
    for col in mi_db.COL_TITLE:
        d, v = mi_db.get_recent(index=col)
        recent_mi['date'] = d
        recent_mi[col] = v
    date = datetime.datetime.strptime(recent_mi['date'], '%Y.%m.%d')
    recent_mi['gsratio'] = round(float(recent_mi['gold']) / float(recent_mi['silver']), 2)
    # 이유는 모르겠지만 aud를 분모로 해야함
    recent_mi['audchf'] = round(float(recent_mi['chf']) / float(recent_mi['aud']), 2)

    #  recent_mi : {'aud': '1.2890', 'chf': '0.8979', 'gbond3y': '1.20', 'gold': '1896.80',
    #  'silver': '28.00', 'kosdaq': '986.12', 'kospi': '3247.83', 'sp500': '4226.52', 'usdkrw': '1114.70'
    # , 'wti': '69.23', 'avgper': 20.02, 'yieldgap': 3.8, 'gsratio': 67.74, 'usdidx': 90.07, 'audchf': 1.44}

    logger.info(f'date : {date}')
    logger.info(f'recent_mi : {recent_mi}')
    context = {'date': date, 'recent_mi': recent_mi}

    # prepare graphs
    d = data.ForMarket()
    height = 250
    width = 400
    sizing_mode = 'stretch_width'

    ####################################################################

    # kospi graph
    x, y = d.make_kospi()
    p = graphs.line_chart(x, y, height=height, width=width)
    context['kospi_script'], context['kospi_div'] = graphs.make_code(p)

    # kosdaq graph
    x, y = d.make_kosdaq()
    p = graphs.line_chart(x, y, height=height, width=width)
    context['kosdaq_script'], context['kosdaq_div'] = graphs.make_code(p)

    # sp500 graph
    x, y = d.make_sp500()
    p = graphs.line_chart(x, y, height=height, width=width)
    context['sp500_script'], context['sp500_div'] = graphs.make_code(p)

    ####################################################################

    # gold graph
    x, y = d.make_gold()
    p = graphs.line_chart(x, y, height=height, width=width)
    context['gold_script'], context['gold_div'] = graphs.make_code(p)

    # silver graph
    x, y = d.make_silver()
    p = graphs.line_chart(x, y, height=height, width=width)
    context['silver_script'], context['silver_div'] = graphs.make_code(p)

    # gsratio graph
    x, y = d.make_gold_silver_ratio()
    p = graphs.line_chart(x, y, height=height, width=width)
    context['gsratio_script'], context['gsratio_div'] = graphs.make_code(p)

    ####################################################################

    # gbond3y graph
    x, y = d.make_gbond3y()
    p = graphs.line_chart(x, y, height=height, width=width)
    context['gbond3y_script'], context['gbond3y_div'] = graphs.make_code(p)

    # yieldgap graph
    x, y = d.make_yieldgap()
    p = graphs.line_chart(x, y, height=height, width=width)
    context['yieldgap_script'], context['yieldgap_div'] = graphs.make_code(p)

    # avgper graph
    x, y = d.make_avgper()
    p = graphs.line_chart(x, y, height=height, width=width)
    context['avgper_script'], context['avgper_div'] = graphs.make_code(p)

    ####################################################################

    # usdkrw graph
    x, y = d.make_usdkrw()
    p = graphs.line_chart(x, y, height=height, width=width)
    context['usdkrw_script'], context['usdkrw_div'] = graphs.make_code(p)

    # wti graph
    x, y = d.make_wti()
    p = graphs.line_chart(x, y, height=height, width=width)
    context['wti_script'], context['wti_div'] = graphs.make_code(p)

    # audchf graph
    x, y = d.make_aud_chf_ratio()
    p = graphs.line_chart(x, y, height=height, width=width)
    context['audchf_script'], context['audchf_div'] = graphs.make_code(p)

    ####################################################################

    # dollar index graph
    x, y = d.make_dollar_index()
    p = graphs.line_chart(x, y, height=height, width=width)
    context['usdidx_script'], context['usdidx_div'] = graphs.make_code(p)

    return context

import pprint
from django import template

from util_hj3415 import utils
from db_hj3415 import mongo
from eval_hj3415 import report
from bokeh_hj3415 import data, graphs

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


register = template.Library()


@register.inclusion_tag('report_stock/report.html')
def get_report(code: str):
    # report context
    context = report.for_django(code=code)

    # dart
    try:
        dart_list = mongo.DartByCode(code=code).get_data().to_dict('records')
        dart_list.reverse()
    except KeyError:
        dart_list = []
    context['darts'] = dart_list[:10]

    # context['price_now_tuple'] = Command().cprice(code=code).cur
    context['price_now_tuple'] = utils.get_price_now(code=code)

    # prepare graphs
    d = data.ForReport(code)
    x = d.make_x()
    height = 200
    sizing_mode = 'stretch_width'
    p1 = graphs.line_circle_chart(x, d.make_y_price(), d.make_y_dart(), height=height, sizing_mode=sizing_mode)
    p2 = graphs.line_chart(x, d.make_y_per(), height=height, sizing_mode=sizing_mode)
    p3 = graphs.line_chart(x, d.make_y_pbr(), height=height, sizing_mode=sizing_mode)
    context['graph_price_script'], context['graph_price_div'] = graphs.make_code(p1)
    context['graph_per_script'], context['graph_per_div'] = graphs.make_code(p2)
    context['graph_pbr_script'], context['graph_pbr_div'] = graphs.make_code(p3)

    context['code'] = code
    logger.info(pprint.pformat(context, width=200))
    return context

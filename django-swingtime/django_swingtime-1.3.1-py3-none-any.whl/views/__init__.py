import calendar
from ..conf import swingtime_settings
from .funcs import *  # noqa
from .cbvs import *  # noqa


if swingtime_settings.CALENDAR_FIRST_WEEKDAY is not None:
    calendar.setfirstweekday(swingtime_settings.CALENDAR_FIRST_WEEKDAY)


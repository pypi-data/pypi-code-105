import itertools
import logging
import calendar
from datetime import datetime, timedelta, time

from dateutil import parser
from django import http
from django.db import models
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404, render

from ..models import Event, Occurrence
from .. import utils, forms


__all__ = [
    'EventListing',
    'EventView',
    'OccurrenceView',
    'AddEvent',
    'DayView',
    'TodayView',
    'YearView',
    'MonthView',
]






class EventListing:
    pass


class EventView:
    pass


class OccurrenceView:
    pass


class AddEvent:
    pass


class DateTimeViewMixin:
    timeslot_factory = None

    def get_context_data(
        self,
        dt,
        items=None,
        params=None
    ):
        '''
        Build a time slot grid representation for the given datetime ``dt``. See
        utils.create_timeslot_table documentation for items and params.

        Context parameters:

        ``day``
            the specified datetime value (dt)

        ``next_day``
            day + 1 day

        ``prev_day``
            day - 1 day

        ``timeslots``
            time slot grid of (time, cells) rows

        '''
        timeslot_factory = timeslot_factory or utils.create_timeslot_table
        params = params or {}

        return render(request, template, {
            'day':       dt,
            'next_day':  dt + timedelta(days=+1),
            'prev_day':  dt + timedelta(days=-1),
            'timeslots': timeslot_factory(dt, items, **params)
        })



class DayView:
    template_view = 'swingtime/daily_view.html'

    def get_context_data(self, **kwargs):
        '''
        '''
        year, month, day = self.args[:3]
        # params):
        dt = datetime(int(year), int(month), int(day))
        return _datetime_view(request, template, dt, **params)


class TodayView:

    def today_view(request, template='swingtime/daily_view.html', **params):
        '''
        See documentation for function``_datetime_view``.

        '''
        return _datetime_view(request, template, datetime.now(), **params)


class YearView:
    pass


class MonthView:
    pass

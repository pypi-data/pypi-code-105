import logging

from admin_extra_urls.api import button, ExtraUrlMixin
from admin_extra_urls.mixins import _confirm_action
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.admin.views.main import ChangeList
from django.core.paginator import InvalidPage, Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

from django_db_logging.handlers import DBHandler
from django_db_logging.settings import config

from .models import Record


class PlainPaginator(Paginator):
    def _get_count(self):
        return config.MAX_LOG_ENTRIES  # we never have more than this
    count = property(_get_count)


class CustomChangeList(ChangeList):

    def get_results(self, request):
        super().get_results(request)
        paginator = PlainPaginator(self.queryset, self.list_per_page)
        try:
            result_list = paginator.page(self.page_num).object_list
        except InvalidPage:  # pragma: no cover
            result_list = ()

        self.full_result_count = 0
        self.result_count = paginator.count
        self.result_list = result_list
        self.can_show_all = False
        self.multi_page = True
        self.paginator = paginator
        self.next_page = len(result_list) == self.list_per_page


@admin.register(Record)
class RecordAdmin(ExtraUrlMixin, ModelAdmin):
    list_display = ('timestamp', 'lvl', 'logger', 'message', 'exception')
    list_filter = ('timestamp', 'level',)
    search_fields = ('logger',)
    date_hierarchy = 'timestamp'
    show_full_result_count = False

    def has_add_permission(self, request):
        return False

    def get_changelist(self, request, **kwargs):
        return CustomChangeList

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def lvl(self, instance):
        level = instance.get_level_display()
        return format_html(f'<span class="badge {level}">{level}</span>')
    lvl.short_description = 'Level'

    def exception(self, instance):
        return bool(instance.exc_type)
    exception.short_description = 'Exception'
    exception.boolean = True

    @button(label='Cleanup')
    def cleanup(self, request):
        opts = self.model._meta
        self.model.objects.cleanup()
        self.message_user(request, "Log cleaned")
        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

    @button(label='Empty Log',
            permission=lambda *a: config.ALLOW_TRUNCATE,
            icon="icon-trash icon-white")
    def empty_log(self, request):
        def _action(request):
            self.model.objects.truncate()

        return _confirm_action(self, request, _action,
                               "Confirm deletion whole error log",
                               "Successfully executed",
                               template='admin/django_db_logging/confirm.html', )

    @button(permission=lambda *a: config.ENABLE_TEST_BUTTON)
    def test(self, request):
        opts = self.model._meta
        logger = logging.getLogger('django_db_logging_test_logger')
        logger.propagate = False
        logger.setLevel(logging.INFO)

        handler = DBHandler()
        formatter = logging.Formatter('%(extra_param)s : %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        extra = {'extra_param': 'EXTRA_PARAM'}
        logger.info("DBLogger [INFO] test log entry", extra=extra)
        logger.debug("DBLogger [DEBUG] test log entry", extra=extra)
        logger.error("DBLogger [ERROR] test log entry", extra=extra)
        logger.warning("DBLogger [WARNING] test log entry", extra=extra)
        logger.critical("DBLogger [CRITICAL] test log entry", extra=extra)
        logger.info("DBLogger [INFO] test log entry", extra=extra)

        try:
            raise BaseException("DBLogger [EXCEPTION] test log entry")
        except BaseException as e:
            logger.exception(e, extra=extra)

        return HttpResponseRedirect(reverse(admin_urlname(opts, 'changelist')))

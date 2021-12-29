
import time
import json
import urllib
from functools import update_wrapper

from magic_import import import_from_string

from django import forms
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, request
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib import admin
from django.contrib.admin.utils import lookup_field
from django.contrib.admin.options import csrf_protect_m
from django.contrib.admin.options import TO_FIELD_VAR
from django.contrib.admin.options import unquote
from django.contrib.admin.views.main import ChangeList
from django.contrib.messages.api import get_messages

from django_middleware_global_request.middleware import get_request


def get_power_admin_class():
    admin_class = getattr(settings, "DJANGO_POWER_ADMIN_EXTENDED_CLASS", "django_power_admin.admin.PowerAdmin")
    return import_from_string(admin_class)

# ---------------------------------------------------------------------------------
# Add extra js & css to admin site
# Work with templates/admin/base.html 
# ---------------------------------------------------------------------------------
EXTRA_JS_KEY = "extra_js"
EXTRA_CSS_KEY = "extra_css"

def add_extra_js(js):
    request = get_request()
    if not hasattr(request, EXTRA_JS_KEY):
        setattr(request, EXTRA_JS_KEY, [])
    getattr(request, EXTRA_JS_KEY).append(js)

def add_extra_css(css):
    request = get_request()
    if not hasattr(request, EXTRA_CSS_KEY):
        setattr(request, EXTRA_CSS_KEY, [])
    getattr(request, EXTRA_CSS_KEY).append(css)


class PowerAdmin(admin.ModelAdmin):
    """
    Powered admin base.

    When you are using PowerAdmin, we suggest that you use `get_power_admin_class` to get the base admin class, 
    so that you can extended all your classes with one setting.
    """
    admin_site_namespace = "admin"

    # required by [Add extra context to admin site]
    add_extra_context_admin_view_name = True
    extra_context_admin_view_name_field = "extra_context_admin_view_name"

    # required by [Add row Toolbar to Changelist]
    add_row_odd_even_class = True
    add_row_index_class = True
    add_row_first_class = True
    add_row_last_class = True

    # required by [Add highlight row to ChangeList]
    CHANGE_LIST_HIGHLIGHT_ROW_IDS_KEY = "_change_list_highlight_row_ids"
    highlight_hover_row = False
    highlight_clicked_row = True

    # required by [Add Sort Buttons To Row Toolbar of Changelist]
    enable_change_list_object_toolbar = True
    show_sortable_buttons = True
    django_sort_field = "display_order"
    django_sort_delta = 100
    django_sort_start = 10000

    # required by [Add read & edit switch button]
    EDIT_FLAG = "_edit_flag"
    EDIT_FLAG_READONLY_VALUE = "0"
    REAL_HAS_CHANGE_PERMISSION_KEY = "_real_has_change_permission"
    REAL_HAS_DELETE_PERMISSION_KEY = "_real_has_delete_permission"

    # #################################################################################
    # Get site settings
    # #################################################################################

    def get_extra_view_names(self):
        extra_view_names =  getattr(self, "extra_views", [])
        if not "move_up" in extra_view_names:
            extra_view_names.append("move_up")
        if not "move_down" in extra_view_names:
            extra_view_names.append("move_down")
        return extra_view_names

    def get_extra_change_list_parameters(self, request):
        return getattr(self, "extra_change_list_parameters", [])

    # #################################################################################
    # Util methods
    # #################################################################################

    def get_model_view_url(self, view_name, obj=None):
        """Return str of reversed url
        """
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        args = obj and [obj.pk] or []
        view_url = reverse(f"admin:{app_label}_{model_name}_{view_name}", args=args)
        return view_url

    def is_change_view(self, request, obj=None):
        """Returns True if it's read/add/change view.
        """
        # alreay set _is_read_view/_is_add_view/_is_change_view flag, use it
        is_read_view_flag = getattr(self, "_is_read_view", False)
        is_add_view_flag = getattr(self, "_is_add_view", False)
        is_change_view_flag = getattr(self, "_is_change_view", False)
        if is_read_view_flag or is_add_view_flag or is_change_view_flag:
            return True
        # try to test the request.path
        if obj:
            change_view_url = self.get_model_view_url("change", obj)
            if change_view_url == request.path:
                return True
            else:
                return False
        # So we not sure
        return False

    def get_messages(self):
        """Returns (loaded_messages, queued_messages)
        """
        request = get_request()
        mss = get_messages(request)
        _loaded_messages = getattr(mss, "_loaded_messages", [])
        _queued_messages = getattr(mss, "_queued_messages", [])
        return _loaded_messages, _queued_messages

    # #################################################################################
    # Functional methods
    # #################################################################################

    # ---------------------------------------------------------------------------------
    # Set view flags
    # ---------------------------------------------------------------------------------
    def set_view_flags(self, is_changelist_view=False, is_read_view=False, is_add_view=False, is_change_view=False, is_delete_view=False, is_history_view=False, is_move_up_view=False, is_move_down_view=False):
        request = get_request()
    
        setattr(request, "_is_changelist_view", is_changelist_view)
        setattr(request, "_is_read_view", is_read_view)
        setattr(request, "_is_add_view", is_add_view)
        setattr(request, "_is_change_view", is_change_view)
        setattr(request, "_is_delete_view", is_delete_view)
        setattr(request, "_is_history_view", is_history_view)
        setattr(request, "_is_move_up_view", is_move_up_view)
        setattr(request, "_is_move_down_view", is_move_down_view)

        if is_changelist_view:
            setattr(request, "_view_name", "changelist_view")
        if is_read_view:
            setattr(request, "_view_name", "read_view")
        if is_add_view:
            setattr(request, "_view_name", "add_view")
        if is_change_view:
            setattr(request, "_view_name", "change_view")
        if is_delete_view:
            setattr(request, "_view_name", "delete_view")
        if is_history_view:
            setattr(request, "_view_name", "history_view")
        if is_move_up_view:
            setattr(request, "_view_name", "move_up_view")
        if is_move_down_view:
            setattr(request, "_view_name", "move_down_view")
    # ---------------------------------------------------------------------------------
    # Views hooks, There are 6 views
    # changelist view
    # read view
    # add view
    # change view
    # delete view
    # history view
    # ---------------------------------------------------------------------------------
    def pre_all_view(self, **kwargs):
        pass

    def post_all_view(self, **kwargs):
        pass

    def pre_changelist_view(self, request, extra_context=None):
        self.pre_all_view(request=request, extra_context=extra_context)

    def post_changelist_view(self, changelist_view_result, request, extra_context=None):

        # required by: [Add Row Classes to ChangeList]
        extra_js = self.get_changelist_object_row_classes_javascript()
        add_extra_js(extra_js)

        self.post_all_view(view_result=changelist_view_result, changelist_view_result=changelist_view_result, request=request, extra_context=extra_context)
        return changelist_view_result

    def pre_read_view(self, request, object_id=None, form_url='', extra_context=None):
        self.pre_all_view(request=request, object_id=object_id, form_url=form_url, extra_context=extra_context)

    def post_read_view(self, read_view_result, request, object_id=None, form_url='', extra_context=None):
        self.post_all_view(view_result=read_view_result, read_view_result=read_view_result, request=request, object_id=object_id, form_url=form_url, extra_context=extra_context)
        return read_view_result

    def pre_add_view(self, request, form_url='', extra_context=None):
        self.pre_all_view(request=request, form_url=form_url, extra_context=extra_context)

    def post_add_view(self, add_view_result, request, form_url='', extra_context=None):
        self.post_all_view(view_result=add_view_result, add_view_result=add_view_result, request=request, form_url=form_url, extra_context=extra_context)
        return add_view_result

    def pre_change_view(self, request, object_id, form_url='', extra_context=None):
        self.pre_all_view(request=request, object_id=object_id, form_url=form_url, extra_context=extra_context)

    def post_change_view(self, change_view_result, request, object_id, form_url='', extra_context=None):
        self.post_all_view(view_result=change_view_result, change_view_result=change_view_result, request=request, object_id=object_id, form_url=form_url, extra_context=extra_context)
        return change_view_result

    def pre_delete_view(self, request, object_id, extra_context=None):
        self.pre_all_view(request=request, object_id=object_id, extra_context=extra_context)

    def post_delete_view(self, delete_view_result, request, object_id, extra_context=None):
        self.post_all_view(view_result=delete_view_result, delete_view_result=delete_view_result, request=request, object_id=object_id, extra_context=extra_context)
        return delete_view_result

    def pre_history_view(self, request, object_id, extra_context=None):
        self.pre_all_view(request=request, object_id=object_id, extra_context=extra_context)
    
    def post_history_view(self, history_view_result, request, object_id, extra_context=None):
        self.post_all_view(view_result=history_view_result, history_view_result=history_view_result, request=request, object_id=object_id, extra_context=extra_context)
        return history_view_result

    def pre_move_up_view(self, request, object_id, extra_context=None):
        self.pre_all_view(request=request, object_id=object_id, extra_context=extra_context)

    def post_move_up_view(self, move_up_view_result, request, object_id, extra_context=None):
        self.post_all_view(view_result=move_up_view_result, history_view_result=move_up_view_result, request=request, object_id=object_id, extra_context=extra_context)
        return move_up_view_result

    def pre_move_down_view(self, request, object_id, extra_context=None):
        self.pre_all_view(request=request, object_id=object_id, extra_context=extra_context)

    def post_move_down_view(self, move_down_view_result, request, object_id, extra_context=None):
        self.post_all_view(view_result=move_down_view_result, history_view_result=move_down_view_result, request=request, object_id=object_id, extra_context=extra_context)
        return move_down_view_result

    # ---------------------------------------------------------------------------------
    # Add extra context to admin site
    # ---------------------------------------------------------------------------------
    def get_extra_context(self, request, **kwargs):
        extra_context = {}
        if self.add_extra_context_admin_view_name:
            extra_context[self.extra_context_admin_view_name_field] = getattr(request, "_view_name")
        return extra_context

    def get_changelist_view_extra_context(self, request, extra_context=None):
        return self.get_extra_context(request, extra_context=extra_context)
    
    def get_read_view_extra_context(self, request, object_id, form_url='', extra_context=None):
        return self.get_extra_context(request, object_id=object_id, form_url=form_url, extra_context=extra_context)
    
    def get_add_view_extra_context(self, request, form_url, extra_context=None):
        return self.get_extra_context(request, form_url=form_url, extra_context=extra_context)

    def get_change_view_extra_context(self, request, object_id, form_url='', extra_context=None):
        return self.get_extra_context(request, object_id=object_id, form_url=form_url, extra_context=extra_context)

    def get_delete_view_extra_context(self, request, object_id, extra_context=None):
        return self.get_extra_context(request, object_id=object_id, extra_context=extra_context)

    def get_history_view_extra_context(self, request, object_id, extra_context=None):
        return self.get_extra_context(request, object_id=object_id, extra_context=extra_context)

    def get_move_up_view_extra_context(self, request, object_id, extra_context=None):
        return self.get_extra_context(request, object_id=object_id, extra_context=extra_context)

    def get_move_down_view_extra_context(self, request, object_id, extra_context=None):
        return self.get_extra_context(request, object_id=object_id, extra_context=extra_context)

    # ---------------------------------------------------------------------------------
    # Add extra view
    # ---------------------------------------------------------------------------------
    def get_extra_view_urls(self):
        urlpatterns = []
        for key in self.get_extra_view_names():
            view = getattr(self, key, None)
            if view and callable(view):
                view_name = getattr(view, "name", key)
                is_object_view = getattr(view, "is_object_view", False)
                url = getattr(view, "url", None)
                if not url:
                    if is_object_view:
                        url = "<path:object_id>/{0}/".format(view_name)
                    else:
                        url = view_name + "/"
                urlpatterns.append(self.make_urlpattern({
                    "name": self.get_admin_view_name(view_name),
                    "view": self.admin_view_wrap(view),
                    "url": url,
                }))
        return urlpatterns

    def admin_view_response_handler(self, view):
        def wrapper(*args, **kwargs):
            result = view(*args, **kwargs)
            if isinstance(result, HttpResponse):
                return result
            elif result is None:
                request = get_request()
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            elif isinstance(result, str):
                return HttpResponseRedirect(result)
            else:
                return JsonResponse(result)
        return wrapper

    def admin_view_wrap(self, view):
        def wrapper(*args, **kwargs):
            result = self.admin_site.admin_view(self.admin_view_response_handler(view))(*args, **kwargs)
            return result
        wrapper.model_admin = self
        return update_wrapper(wrapper, view)

    def get_admin_view_name(self, view_name):
        if not isinstance(view_name, str):
            view_name = getattr(view_name, "name", view_name.__name__)
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return "{app_label}_{model_name}_{view_name}".format(app_label=app_label, model_name=model_name, view_name=view_name)

    def get_admin_view_name_full(self, view_name):
        view_name = self.get_admin_view_name(view_name)
        view_name_full = "{namespace}:{view_name}".format(namespace=self.admin_site_namespace, view_name=view_name)
        return view_name_full

    def make_urlpattern(self, config):
        from django.urls import path

        name = config.get("name", None)
        view = config["view"]
        url = config["url"]

        if isinstance(view, str):
            view = getattr(self, view, None)
            if view is None:
                view = import_from_string(view)
        
        extra_params = {}
        if name:
            extra_params["name"] = name
        return path(url, self.admin_view_wrap(view), **extra_params)

    def get_view_url(self, view, object_id=None):
        view_name_full = self.get_admin_view_name_full(view)
        is_object_view = getattr(view, "is_object_view", False)
        if is_object_view:
            return reverse(view_name_full, kwargs={"object_id": object_id})
        else:
            return reverse(view_name_full)

    def is_extra_view(self, view):
        return getattr(view, "extra_view", False)

    # ---------------------------------------------------------------------------------
    # Add row Toolbar to Changelist
    # ---------------------------------------------------------------------------------
    list_display_links = None

    def get_change_list_object_toolbar_buttons(self, buttons_var_name, obj):
        buttons = []
        change_list_object_toolbar_buttons = getattr(self, buttons_var_name, ["read_button", "change_button", "delete_button"])
        for button in change_list_object_toolbar_buttons:
            f, attr, value = lookup_field(button, obj, self)
            buttons.append({
                "f": f,
                "attr": attr,
                "value": value,
            })
        return buttons

    def change_list_object_toolbar(self, obj):
        return self.make_change_list_object_toolbar("change_list_object_toolbar_buttons", obj)
    change_list_object_toolbar.short_description = _("Operations")

    def make_change_list_object_toolbar(self, obj, buttons_var_name):
        buttons = self.get_change_list_object_toolbar_buttons(obj, buttons_var_name)
        request = get_request()
        return render_to_string("django_power_admin/admin/ChangeListObjectToolbarButtons.html", {
            "buttons": buttons,
            "request": request,
        })

    def read_button(self, obj):
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        url = reverse(f"admin:{app_label}_{model_name}_change", args=[obj.pk]) + "?_edit_flag=0"
        label = _("Read")
        return format_html("""<a class="viewlink" href="{url}">{label}</a>""", url=url, label=label)
    read_button.short_description = _("Read")

    def change_button(self, obj):
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        url = reverse(f"admin:{app_label}_{model_name}_change", args=[obj.pk]) + "?_edit_flag=1"
        label = _("Change")
        return format_html("""<a class="changelink" href="{url}">{label}</a>""", url=url, label=label)
    change_button.short_description = _("Change")

    def delete_button(self, obj):
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        url = reverse(f"admin:{app_label}_{model_name}_delete", args=[obj.pk])
        label = _("Delete")
        return format_html("""<a class="deletelink" href="{url}">{label}</a>""", url=url, label=label)
    delete_button.short_description = _("Delete")

    # We say view something
    # Now we say read something
    # Keep the old name so that old things goes well
    view_action = read_button
    read_action = read_button
    edit_action = change_button
    edit_button = change_button
    change_action = change_button
    delete_action = delete_button

    # ---------------------------------------------------------------------------------
    # Add Row Classes to ChangeList
    # ---------------------------------------------------------------------------------
    def get_changelist_object_row_classes_javascript(self):
        request = get_request()
        objs = getattr(request, "_changelist_instance").result_list
        javascripts = []
        index = 0
        for obj in objs:
            class_text = " ".join(self.get_object_row_class(obj, index, objs))
            if class_text:
                javascripts.append("""
                $("#result_list .action-select[value={pk}]").parents("tr").addClass("{class_text}");
                """.format(pk=obj.pk, class_text=class_text))
            index += 1
        if javascripts:
            return """
            $(document).ready(function(){{
                {javascript_text}
            }});
            """.format(javascript_text="\n".join(javascripts))
        else:
            return ""

    def get_object_row_class(self, obj, index, objs):
        classes = []

        # add basic classes to changelist rows
        if self.add_row_odd_even_class:
            if index % 2 == 0:
                classes.append("result_list_row_odd")
            else:
                classes.append("result_list_row_even")
        if self.add_row_index_class:
            classes.append("result_list_row_index_{index}".format(index=index))
        if self.add_row_first_class and index == 0:
            classes.append("result_list_first_row")
        if self.add_row_last_class and index == len(objs) - 1:
            classes.append("result_list_last_row")
        
        # By default, highlight_hover_row is disabled
        # so that it will NOT mass up with move_up&move_down highlights
        # You can enable it by set TheAdminSite's `highlight_hover_row` property to True
        if self.highlight_hover_row:
            classes.append("highlight_hover_row_enabled")
    
        # By default, highlight_clicked_row is enabled
        # You can disable it by set TheAdminSite's `highlight_clicked_row` property to False
        if self.highlight_clicked_row:
            classes.append("highlight_clicked_row_enabled")

        # add `change_list_highlight_row` class to changelist rows
        # required by [Add highlight row to ChangeList]
        highlight_row_ids =  self.get_highlight_row_ids()
        if highlight_row_ids:
            print("*"*10, highlight_row_ids, type(highlight_row_ids[0]), obj.pk)
        if obj.pk in highlight_row_ids:
            classes.append("change_list_highlight_row")
        
        return classes

    # ---------------------------------------------------------------------------------
    # Add highlight row to ChangeList
    # ---------------------------------------------------------------------------------
    def set_change_list_highlight_rows(self, rows):
        request = get_request()
        request.session[self.CHANGE_LIST_HIGHLIGHT_ROW_IDS_KEY] = json.dumps(rows)

    def get_highlight_row_ids(self):
        request = get_request()
        if hasattr(request, self.CHANGE_LIST_HIGHLIGHT_ROW_IDS_KEY):
            return getattr(request, self.CHANGE_LIST_HIGHLIGHT_ROW_IDS_KEY)
        highlight_row_ids = json.loads(request.session.get(self.CHANGE_LIST_HIGHLIGHT_ROW_IDS_KEY, "[]"))
        setattr(request, self.CHANGE_LIST_HIGHLIGHT_ROW_IDS_KEY, highlight_row_ids)
        if self.CHANGE_LIST_HIGHLIGHT_ROW_IDS_KEY in request.session:
            del request.session[self.CHANGE_LIST_HIGHLIGHT_ROW_IDS_KEY]
        return highlight_row_ids

    # ---------------------------------------------------------------------------------
    # Add Sort Buttons To Row Toolbar of Changelist
    # ---------------------------------------------------------------------------------

    sortable_admin_sort_arrows = [
        "move_up_arrow",
        "move_down_arrow",
    ]

    def sort_arrows(self, obj):
        return self.make_change_list_object_toolbar("sortable_admin_sort_arrows", obj)
    sort_arrows.short_description = _("Sortable Admin Sortable Arrows")

    def move_up_arrow(self, obj):
        url = self.get_view_url(self.move_up, obj.pk)
        label = _("Move Up")
        return format_html("""<a class="sortable_admin_move_up_arrow" href="{url}"><i class="fa fa-arrow-up"></i>&nbsp;{label}</a>""", url=url, label=label)
    move_up_arrow.short_description = _("Move Up")

    def move_down_arrow(self, obj):
        url = self.get_view_url(self.move_down, obj.pk)
        label = _("Move Down")
        return format_html("""<a class="sortable_admin_move_down_arrow" href="{url}"><i class="fa fa-arrow-down"></i>&nbsp;{label}</a>""", url=url, label=label)
    move_up_arrow.short_description = _("Move Down")

    def reset_order(self):
        objs = self.model.objects.all()
        index = self.django_sort_start
        for obj in objs:
            setattr(obj, self.django_sort_field, index)
            index += self.django_sort_delta
        return self.model.objects.bulk_update(objs, [self.django_sort_field])

    def move_up(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        self.set_view_flags(is_move_up_view=True)
        extra_context.update(self.get_move_up_view_extra_context(request=request, object_id=object_id, extra_context=extra_context))
        self.pre_move_up_view(request=request, object_id=object_id, extra_context=extra_context)

        object_id = int(object_id)
        obj = self.get_object(request, object_id)
        values = self.get_queryset(request).values_list("id", self.django_sort_field)
        prev_value = None
        self.set_change_list_highlight_rows([obj.pk])
        for index, value in enumerate(values):
            if obj.pk == value[0]:
                if index == 0:
                    prev_id = None
                    prev_value = None
                else:
                    prev_id = values[index-1][0]
                    prev_value = values[index-1][1]
        if prev_id is None:
            messages.error(request, _("This item is already the first."))
        else:
            obj_value = getattr(obj, self.django_sort_field)
            if prev_value != obj_value:
                prev = self.model.objects.get(pk=prev_id)
                setattr(obj, self.django_sort_field, prev_value)
                setattr(prev, self.django_sort_field, obj_value)
                self.model.objects.bulk_update([obj, prev], [self.django_sort_field])
            else:
                self.reset_order()
                obj = self.model.objects.get(pk=object_id)
                prev = self.model.objects.get(pk=prev_id)
                obj_value = getattr(obj, self.django_sort_field)
                prev_value = getattr(prev, self.django_sort_field)
                setattr(obj, self.django_sort_field, prev_value)
                setattr(prev, self.django_sort_field, obj_value)
                self.model.objects.bulk_update([obj, prev], [self.django_sort_field])
            messages.success(request, _("Item move up done!"))
    move_up.is_object_view = True
    move_up.name = "move_up"

    def move_down(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        self.set_view_flags(is_move_down_view=True)
        extra_context.update(self.get_move_down_view_extra_context(request=request, object_id=object_id, extra_context=extra_context))
        self.pre_move_down_view(request=request, object_id=object_id, extra_context=extra_context)

        object_id = int(object_id)
        obj = self.get_object(request, object_id)
        values = self.get_queryset(request).values_list("id", self.django_sort_field)
        next_value = None
        self.set_change_list_highlight_rows([obj.pk])
        for index, value in enumerate(values):
            if obj.pk == value[0]:
                if index == len(values) - 1:
                    next_id = None
                    next_value = None
                else:
                    next_id = values[index+1][0]
                    next_value = values[index+1][1]
        if next_id is None:
            messages.error(request, _("This item is already the last."))
        else:
            obj_value = getattr(obj, self.django_sort_field)
            if next_value != obj_value:
                next = self.model.objects.get(pk=next_id)
                setattr(obj, self.django_sort_field, next_value)
                setattr(next, self.django_sort_field, obj_value)
                self.model.objects.bulk_update([obj, next], [self.django_sort_field])
            else:
                self.reset_order()
                obj = self.model.objects.get(pk=object_id)
                next = self.model.objects.get(pk=next_id)
                obj_value = getattr(obj, self.django_sort_field)
                next_value = getattr(next, self.django_sort_field)
                setattr(obj, self.django_sort_field, next_value)
                setattr(next, self.django_sort_field, obj_value)
                self.model.objects.bulk_update([obj, next], [self.django_sort_field])
            messages.success(request, _("Item move down done!"))
    move_down.is_object_view = True
    move_down.name = "move-down"

    # ---------------------------------------------------------------------------------
    # Add read & edit switch button
    # ---------------------------------------------------------------------------------
    def has_change_permission_real(self, request, obj=None):
        self.has_change_permission(request, obj)
        return getattr(request, self.REAL_HAS_CHANGE_PERMISSION_KEY, None)

    def has_delete_permission_real(self, request, obj=None):
        self.has_delete_permission(request, obj)
        return getattr(request, self.REAL_HAS_DELETE_PERMISSION_KEY, None)

    def has_change_permission(self, request, obj=None):
        """Disable change permission in read_view.

        `change_view` without `edit_flag` is a read view.
        `change_view` without change permission is a read view.

        `change_view` has both `edit_flag` and `change permission` is a change view.
        """
        result = super().has_change_permission(request, obj=obj)
        setattr(request, self.REAL_HAS_CHANGE_PERMISSION_KEY, result)
        if self.is_change_view(request, obj) and request.GET.get(self.EDIT_FLAG, self.EDIT_FLAG_READONLY_VALUE) == self.EDIT_FLAG_READONLY_VALUE:
            return False
        else:
            return result
    
    def has_delete_permission(self, request, obj=None):
        """Disable delete permission in read_view.
        """
        result = super().has_delete_permission(request, obj=obj)
        setattr(request, self.REAL_HAS_DELETE_PERMISSION_KEY, result)
        if self.is_change_view(request, obj) and request.GET.get(self.EDIT_FLAG, self.EDIT_FLAG_READONLY_VALUE) == self.EDIT_FLAG_READONLY_VALUE:
            return False
        else:
            return result
    # #################################################################################
    # ModelAdmin overrides
    # #################################################################################

    # changelist view entry point
    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        extra_context = {}
        self.set_view_flags(is_changelist_view=True)
        extra_context.update(self.get_changelist_view_extra_context(request=request, extra_context=extra_context))
        self.pre_changelist_view(request=request, extra_context=extra_context)
        changelist_view_result = super().changelist_view(request=request, extra_context=extra_context)
        changelist_view_result = self.post_changelist_view(changelist_view_result=changelist_view_result, request=request, extra_context=extra_context)
        return changelist_view_result

    # read, add and change view entry point
    @csrf_protect_m
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        is_read_view = False
        is_add_view = False
        is_change_view = False

        if object_id is None:
            # add view
            is_add_view = True
            self.set_view_flags(is_add_view=True)
            extra_context.update(self.get_add_view_extra_context(request=request, form_url=form_url, extra_context=extra_context))
            self.pre_add_view(request=request, form_url=form_url, extra_context=extra_context)
        else:
            obj = self.get_object(request, object_id)
            if self.has_change_permission(request, obj):
                # change view
                is_change_view = True
                self.set_view_flags(is_change_view=True)
                extra_context.update(self.get_change_view_extra_context(request=request, object_id=object_id, form_url=form_url, extra_context=extra_context))
                self.pre_change_view(request=request, object_id=object_id, form_url=form_url, extra_context=extra_context)
            else:
                # read view
                is_read_view = True
                self.set_view_flags(is_read_view=True)
                extra_context.update(self.get_read_view_extra_context(request=request, object_id=object_id, form_url=form_url, extra_context=extra_context))
                self.pre_read_view(request=request, object_id=object_id, form_url=form_url, extra_context=extra_context)

        changeform_result = super().changeform_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context)

        if is_add_view:
            return self.post_add_view(add_view_result=changeform_result, request=request, form_url=form_url, extra_context=extra_context)
        if is_change_view:
            return self.post_change_view(change_view_result=changeform_result, request=request, object_id=object_id, form_url=form_url, extra_context=extra_context)
        if is_read_view:
            return self.post_read_view(read_view_result=changeform_result, request=request, object_id=object_id, form_url=form_url, extra_context=extra_context)

        # always not reachable here...
        return changeform_result

    # delete view entry point
    @csrf_protect_m
    def delete_view(self, request, object_id, extra_context=None):
        extra_context = {}
        self.set_view_flags(is_delete_view=True)
        extra_context.update(self.get_delete_view_extra_context(request=request, object_id=object_id, extra_context=extra_context))
        self.pre_delete_view(request=request, object_id=object_id, extra_context=extra_context)
        delete_view_result = super().delete_view(request=request, object_id=object_id, extra_context=extra_context)
        delete_view_result = self.post_delete_view(delete_view_result=delete_view_result, request=request, object_id=object_id, extra_context=extra_context)
        return delete_view_result

    # history entry point
    def history_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        self.set_view_flags(is_history_view=True)
        extra_context.update(self.get_history_view_extra_context(request=request, object_id=object_id, extra_context=extra_context))
        self.pre_history_view(request=request, object_id=object_id, extra_context=extra_context)
        history_view_result = super().history_view(request=request, object_id=object_id, extra_context=extra_context)
        history_view_result = self.post_history_view(history_view_result=history_view_result, request=request, object_id=object_id, extra_context=extra_context)
        return history_view_result

    def get_urls(self):
        urlpatterns = self.get_extra_view_urls()
        urlpatterns += super().get_urls()
        return urlpatterns

    def get_changelist_instance(self, request):
        result = super().get_changelist_instance(request)
        setattr(request, "_changelist_instance", result)
        return result

    def get_changelist(self, request, **kwargs):
        modeladmin = self
        class IgnoreExtraParametersChangeList(ChangeList):
            def __init__(self, request, *args, **kwargs):
                super().__init__(request, *args, **kwargs)
                self._extra_change_list_parameters = {}
                for name in modeladmin.get_extra_change_list_parameters(request):
                    self._extra_change_list_parameters[name] = self.params.get(name, None)

            def get_queryset(self, request):
                for name in modeladmin.get_extra_change_list_parameters(request):
                    if name in self.params:
                        del self.params[name]
                print("get_queryset", self.params)
                queryset = super().get_queryset(request)
                return queryset
        return IgnoreExtraParametersChangeList

    def get_list_display(self, request):
        """
        if `enable_change_list_object_toolbar==True`, append `change_list_object_toolbar` field to `list_display`
        """
        fields = super().get_list_display(request)
        if self.enable_change_list_object_toolbar:
            if not "change_list_object_toolbar" in fields:
                fields = list(fields) + ["change_list_object_toolbar"]
        return fields

    class Media:
        css = {
            "all": [
                "fontawesome/css/all.min.css",
                "django_power_admin/admin/css/ChangeListHighlightRow.css",
                "django_power_admin/admin/css/ChangeListObjectToolbar.css",
                "django_power_admin/admin/css/Sortable.css",
            ]
        }
        js = [
            "admin/js/vendor/jquery/jquery.js",
            "django_power_admin/admin/js/ChangeListHighlightRow.js",
            "admin/js/jquery.init.js",
        ]    
    # #################################################################################
    # End of PowerAdmin
    # #################################################################################



"""
class SimpleExportAdmin(ChangeFormObjectToolbarAdmin):
    
    def simple_export(self):
        pass
    simple_export.short_description = _("Export")
    simple_export.icon = "fa fa-export"

class SimpleImportAdmin(ChangeFormObjectToolbarAdmin):
    
    def simple_import(self):
        pass
    simple_import.short_description = _("Import")
    simple_import.icon = "fa fa-import"

    class Media:
        css = {
            "all": [
                "django-power-admin/admin/SimpleImportAdmin/css/SimpleImportAdmin.css",
            ]
        }
        js = [
            "admin/js/vendor/jquery/jquery.js",
            "django_power_admin/admin/SimpleImportAdmin/js/SimpleImportAdmin.js",
            "admin/js/jquery.init.js",
        ]
"""
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse


class PmedienDefaults(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if self.model.objects.all().count() == 1:
            obj = self.model.objects.first()
            return HttpResponseRedirect(
                reverse("admin:%s_%s_change" % (self.model._meta.app_label, self.model._meta.model_name),
                        args=(obj.id,)))
        else:
            return HttpResponseRedirect(
                reverse("admin:%s_%s_add" % (self.model._meta.app_label, self.model._meta.model_name)))

    def get_form(self, request, obj=None, **kwargs):
        return super(PmedienDefaults, self).get_form(request, obj, **kwargs)

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        if self.model.objects.count() == 0:
            return True
        else:
            return False

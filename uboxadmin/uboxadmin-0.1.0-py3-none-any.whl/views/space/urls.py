from uboxadmin.generic import new_simple_model_viewset
from uboxadmin.models.space import AppSpaceInfo, AppSpaceType

urlpatterns = []

new_simple_model_viewset(AppSpaceInfo).register_to(urlpatterns, "info/")
new_simple_model_viewset(AppSpaceType).register_to(urlpatterns, "type/")

from django.utils.module_loading import autodiscover_modules

from uboxadmin.generic import Router

router = Router()

autodiscover_modules("uboxadmin")

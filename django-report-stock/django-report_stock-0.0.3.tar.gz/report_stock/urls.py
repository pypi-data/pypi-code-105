from django.urls import path
from .views import test

app_name = 'report_stock'

urlpatterns = [
    path('', test, name='test'),
]

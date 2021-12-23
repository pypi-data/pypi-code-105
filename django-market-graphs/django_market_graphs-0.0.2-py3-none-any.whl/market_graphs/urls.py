from django.urls import path
from .views import test

app_name = 'market_hj3415'

urlpatterns = [
    path('', test, name='test'),
]

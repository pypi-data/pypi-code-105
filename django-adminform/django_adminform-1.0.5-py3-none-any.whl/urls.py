from django.urls import path
from . import views


app_name = 'django_adminform'

urlpatterns = [
    path('upload/', views.upload_handler, name='upload'),
]
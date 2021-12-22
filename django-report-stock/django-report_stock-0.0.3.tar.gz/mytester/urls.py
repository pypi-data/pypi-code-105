from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fav_stock/', include('fav_stock.urls', namespace='fav_stock')),
    path('', include('report_stock.urls')),
]

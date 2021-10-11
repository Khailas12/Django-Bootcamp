from django.contrib import admin
from django.urls import path, include
from myapp.views import home_view, product_detail_view, product_json_view


urlpatterns = [
    path('search/', home_view, name='home'),
    path('product/<int:id>/', product_detail_view, name='productdetails'),
    path('product/json/', product_json_view, name='prodjson'),
    path('admin/', admin.site.urls),
]
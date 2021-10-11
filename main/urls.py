from django.contrib import admin
from django.urls import path, include, re_path #url
from myapp.views import home_view, product_detail_view, product_json_view


urlpatterns = [
    path('search/', home_view, name='home'),
    path('product/<int:pk>/', product_detail_view, name='productdetails'),  # pk -> primary key
    # path('productjson/<int:id>/', product_json_view, name='productjson'),
    re_path(r'productjson/(?P<pk>\d+)/', product_json_view, name='prodjson'),
    path('admin/', admin.site.urls),
]
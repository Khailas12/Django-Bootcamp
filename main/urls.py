from django.contrib import admin
from django.urls import path, include, re_path  #url
from django.views.generic import TemplateView

from myapp.views import (
    home_view, product_detail_view, product_json_view, product_list_view, product_create_view
    )

from accounts.views import (
    login_view, logout_view, register_view
    )


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('product/<int:pk>/', product_detail_view, name='productdetails'),  # pk -> primary key
    # path('productjson/<int:id>/', product_json_view, name='productjson'),
    
    re_path(r'productjson/(?P<pk>\d+)/', product_json_view, name='prodjson'),
    path('productlist/', product_list_view, name='prodlist'),
    path('product/create/', product_create_view, name='create'),
    
    # from accounts.view
    path('login/', login_view, name='login'),  
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
     
    path('admin/', admin.site.urls),
]
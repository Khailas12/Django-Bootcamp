from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from myapp.models import Product


def home_view(request, *args, **kwargs):
    return HttpResponse("<h1>Hello world</h1>")


def product_detail_view(request, id):  
    obj = Product.objects.get(id=id) 
    try: 
        obj = Product.objects.get(id=id)
    except Product.DoesNotExist:    # this handles whether it exists or not
        raise Http404('Product does not exist')
    return HttpResponse(f'Product id {obj.id}')


def product_json_view(request, *args, **kwargs):
    obj = Product.objects.get(id=1)
    return JsonResponse({'id': obj.id })
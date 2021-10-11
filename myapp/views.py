from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from myapp.models import Product


def home_view(request, *args, **kwargs):
    context = {
        'name': 'bruce'
    }
    return render(request, 'home.html', context)


def product_detail_view(request, pk, *args, **kwargs):
    # obj = Product.objects.get(pk=pk)

    try:
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:    # this handles whether it exists or not
        raise Http404('Product does not exist')

    context = {
        'object': obj
    }
    return render(request, 'products/detail.html', context)


def product_json_view(request, pk,  *args, **kwargs):
    try:
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Not Found'})
    return JsonResponse({'pk': obj.pk})
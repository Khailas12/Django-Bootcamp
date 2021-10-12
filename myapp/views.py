from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from .models import Product
from .forms import ProductForm


# def bad_view(request, *args, **kwargs):
#     print(request.GET)
#     my_request_data = dict(request.GET)
#     new_produdct = my_request_data.get('new product')
#     print(my_request_data, new_produdct)

#     if new_produdct[0].lower() == 'true':
#         print('new prod')
#         Product.objects.create(title=my_request_data.get('title')[0], content=my_request_data.get('content')[0])
#     return HttpResponse('bad view')


def home_view(request, *args, **kwargs):
    query = request.GET.get('q')
    print(query)
    # queryset = Product.objects.filter(query[0])
    context = {
        'name': 'bruce',
        'query': query
    }
    return render(request, 'home.html', context)


# def product_create_view(request, *args, **kwargs):
#     print(request.POST)
#     print(request.GET)
#     if request.method == 'POST':
#         post_data = request.POST or None

#         if post_data != None:
#             prod_form = ProductForm(request.POST)
#             if prod_form.is_valid():
#                 title_from_input = prod_form.cleaned_data.get('title')
#                 Product.objects.create(title=title_from_input)

#     context = {}
#     return render(request, 'products/forms.html', context)

# this makes it easier compared to the one above to get rid of hard coding base.
# def product_create_view(request, *args, **kwargs):
#     form = ProductForm(request.POST or None)  
#     if form.is_valid():
#         print(form.cleaned_data)    # cleaned_data returns a dictionary of validated form input fields and their values, where string primary keys are returned as objects. where validation keys are stored.
#         data = form.cleaned_data
#         Product.objects.create(**data)
        
#     context = {
#         'form': form
#     }
#     return render(request, 'products/forms.html', context)


#this is the much standard and simplified version of the 2 ones above.
def product_create_view(request, *args, **kwargs):
    form = ProductForm(request.POST or None)      # None excludes the validation errors
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        
        form = ProductForm()
    
    context = {
        'form': form
    }
    return render(request, 'products/forms.html', context)


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


def product_list_view(request, *args, **kwargs):
    # to iterate through it. the iteration is done in the html.
    queryset = Product.objects.all()
    context = {'obj_list': queryset}
    return render(request, 'products/list_iteration.html', context)

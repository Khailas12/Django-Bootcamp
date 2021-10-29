from django.http.response import Http404
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.admin.views.decorators import staff_member_required     # alternative to login_required

from emails.forms import InventoryWaitlistForm
from .models import Product
from .forms import ProductForm


def product_featured_view(request, *args, **kwargs):
    queryset = Product.objects.filter(featured=True)
    product = None
    can_order = False
    form = None
    
    if queryset.exists():
        product = queryset.first()
    
    if product != None:
        can_order = product.can_order
        if can_order:
            product_id = product.id
            request.session['product_id'] = product_id
        
        form = InventoryWaitlistForm(request.POST or None, product=product) 
        if form.is_valid():
            obj = form.save(commit=False)
            obj.product = product
            
            if request.user.is_authenticated:
                obj.user = request.user
            obj.save()
            return redirect('/waitlist-success')
        
    context = {
        'product': product,
        'can_order': can_order,
        'email_form': form,
    }
    return render(request, 'products/featured.html', context)


def home_view(request, *args, **kwargs):
    query = request.GET.get('q')
    print(query)
    # queryset = Product.objects.filter(query[0])
    context = {
        'name': 'bruce',
        'query': query,
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
@staff_member_required    # it forces to login to the admin page and directs to the page we need
def product_create_view(request, *args, **kwargs):
    # request.FILES = handles the file upload
    form = ProductForm(request.POST or None, request.FILES or None)      # None excludes the validation errors
    if form.is_valid():
        obj = form.save(commit=False)
        
        image = request.FILES.get('image')
        media = request.FILES.get('media')
        # general info: large size would cause server timeout. so the async is used to prevent that. 
        
        if image:
            obj.image = image
        
        if media:
            obj.media = media
        
        obj.user = request.user     # calls from the foreginkey in the models.py
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
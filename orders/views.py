from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Order
from myapp.models import Product
from .forms import OrderForm
from django.http import Http404, HttpResponse, response
import pathlib
from wsgiref.util import FileWrapper
from mimetypes import guess_type    # mimetypes converts btwn a filename or URL and the MIME type associated with the filename extension


@login_required
def order_checkout_view(request, *args, **kwargs):
    queryset = Product.objects.filter(featured=True)    # filters which products they see on a page.
    if not queryset.exists():
        return redirect('/')    # redirects if featured is false or some other reasons.

    product = queryset.first()
    user = request.user
    
    order_id = request.session.get('order_id')
    order_obj = None
    new_creation = False
    
    try:
        order_obj = Order.objects.get(id=order_id)
    except:
        order_id = None
        
    if order_id == None:  # no order id or obj
        new_creation = True
        order_obj = Order.objects.create(product=product, user=user)
        request.session['order_id'] = order_obj.id
        
    if order_obj != None and new_creation == False:
        if order_obj.product.id != product.id:  # has order id
            order_obj = Order.objects.create(product=product, user=user)
    request.session['order_id'] = order_obj.id
    
    form = OrderForm(request.POST or None, product=product, instance=order_obj)
    if form.is_valid():
        order_obj.shipping_address = form.cleaned_data.get('shipping_address')
        order_obj.billing_address = form.cleaned_data.get('billing_address')
        order_obj.save()
        
    context = {
        'form': form,
        'object': order_obj
        }
    return render(request, 'orders/checkout.html', context)


# downloading the media
def download_order(required, *args, **kwargs):
    order_id = 'abc'
    # media__isnull=False makes it to validate whether the media exists or not before calling
    queryset = Product.objects.filter(media__isnull=False)
    product_obj = queryset.first()
    
    if not product_obj.media:
        raise Http404
    
    media = product_obj.media
    product_path = media.path
    path = pathlib.Path(product_path)   # os.path
    
    pk = product_obj.pk     # pk -> primary key
    extension = path.suffix     # extension like .csv, .jpg, .png etc
    file_name = f'The-Product-{order_id}-{pk}{extension}'
    
    
    if not path.exists():
        raise Http404
    
    with open(path,'rb') as f:  # rb mode-> reading as bytes, to send it back as bytes
        wrapper = FileWrapper(f)
        content_type = 'application/force-download'
        guessed_ = guess_type(path)[0]     # it guesses the extension and confirms it
        if guessed_:
            content_type = guessed_
            
        response = HttpResponse(wrapper, content_type=content_type)
        response['Content-Disposition'] = f'attachment;{file_name}'     # this makes the browser to realize to download the file
        response['X-SendFile'] = f'{file_name}'
        return response
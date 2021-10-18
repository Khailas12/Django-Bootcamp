from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Order
from myapp.models import Product
from .forms import OrderForm
from django.http import Http404, HttpResponse
import pathlib
from wsgiref.util import FileWrapper
from mimetypes import guess_type



@login_required
def order_checkout_view(request, *args, **kwargs):
    queryset = Product.objects.filter(featured=True)    # filters which products they see on a page.
    if not queryset.exists():
        return redirect('/')    # redirects if featured is false or some other reasons.

    product = queryset.first()
    # if not product.has_inventory():
    #     return redirect('/no-inventory')
    
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
        
        order_obj.mark_paid(save=False)
        # order_obj.status = 'paid'
        order_obj.save()
        
        del request.session['order_id']  # clears and refreshes the input area after succesful checkouts.
        return redirect('/success')
        
    context = {
        'form': form,
        'object': order_obj
        }
    return render(request, 'orders/checkout.html', context)


# download the product media. it includeds the uploaded one
def download_order(request, *args, **kwargs):
    order_id = 'abc'
    queryset = Product.objects.filter(media__isnull=False)
    product_obj = queryset.first()
    
    if not product_obj.media:
        raise Http404
    
    media = product_obj.media
    product_path = media.path
    path = pathlib.Path(product_path)
    
    pk = product_obj.pk     # primary key
    extension = path.suffix # png, jpg, csv and so on
    file_name = f'The-Product-{order_id}-{pk}{extension}'
    
    if not path.exists():
        raise Http404
    
    with open(path, 'rb') as f:  # rb -> read it in bytes
        wrapper = FileWrapper(f)
        content_type = 'application/force-download'
        
        guessed_ = guess_type(path)[0]    # this opens the file and guess its type
        if guessed_:
            content_type = guessed_
    
        response = HttpResponse(wrapper, content_type='')
        response['Content-Disposition'] = f'attachment;filename={file_name}'    # this lets the browser to know to download this
        response['X-SendFile'] = f'{file_name}'
        return response
        
    return HttpResponse
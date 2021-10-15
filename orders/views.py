from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Order
from myapp.models import Product
from .forms import OrderForm


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
        
    context = {'form': form}
    return render(request, 'products/forms.html', context)

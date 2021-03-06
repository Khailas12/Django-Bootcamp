from django import forms 
from .models import Order


class OrderForm(forms.ModelForm):
    shipping_address = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'shipping-address-class form-control',
            'rows': 4,  # default is 10
            'placeholder': 'Shipping address'
        })
    )
    
    billing_address = forms.CharField(
        label='',
        widget = forms.Textarea(attrs={
            'class': 'billing-address-class form-control',
            'rows': 4,
            'placeholder': 'Billing address'
        })
    )
    
    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product') or None
        super().__init__(*args, **kwargs)   # super is used to inherit from another class ModelFrom
        self.product = product
    
    class Meta:
        model = Order
        fields = [
            'shipping_address',
            'billing_address',
        ]
          
    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        shipping_addr = cleaned_data.get('shipping_address')
        
        # check product inventory
        if self.product != None:
            if not self.product.can_order:
                raise forms.ValidationError('This product cannot be ordered')
        
            if (self.product.requires_shipping and shipping_addr) == '' or (self.product.requires_shipping and shipping_addr == None):
                self.add_error(
                    'shipping address',
                    'Enter your shipping address'
                )
                # raise forms.ValidationError(
                #     'Enter your shipping address'
                # )
        return cleaned_data
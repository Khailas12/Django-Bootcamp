from django import forms 
from .models import Order


class OrderForm(forms.ModelForm):
    shipping_address = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'shipping-address-class form-control',
            'rows': 3,
            'placeholder': 'Your shipping address'
        })
    )
    
    billing_address = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'billing-address-class form-control',
            'rows': 3,
            'placeholder': 'Your billing address here',
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
        # check product inventory
        if self.product != None:
            if not self.product.can_order:
                raise forms.ValidationError('This product cannot be ordered')
            
        return cleaned_data
from django import forms
from .models import InventoryWaitList


class InventoryWaitlistForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product') or None
        super().__init__(*args, **kwargs)
        self.product = product
        
    class Meta:
        model = InventoryWaitList
        fields = [
            'email',
        ]
        
    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        email = cleaned_data.get('email')
        queryset = InventoryWaitList.objects.filter(product=self.product, email__iexact=email)
        
        if queryset.count() > 5:
            error_msg ='10-4 we have your waitlist entry for this product'
            # raise self.add_error('email', error_msg)
            raise forms.ValidationError(error_msg)
        
        return cleaned_data
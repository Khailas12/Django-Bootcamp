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
        queryset = InventoryWaitList.objects.filter(Product=self.product, email__iexact=email)
        
        if queryset.count() > 5:
            raise self.add_error(
                'email', '10-4 we have your waitlist entry for this product'
            )
        
        return cleaned_data
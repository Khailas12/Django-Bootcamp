from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title',
            'content',
            'price',
            'image',
            'media',
        ]
    
     # this is called while during the .is_valid() method
    def clean_title(self): 
        data = self.cleaned_data.get('title')
        if len(data) < 4 :
            raise forms.ValidationError('Minimum 5 characters required')
        return data
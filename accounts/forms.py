from django.contrib.auth import get_user_model
from django import forms


User = get_user_model()     # all follows the one assigned on db using terminal.
not_allowed_username = ['abc']


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'user-password'
            }
        )
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'user-confirm-password'
            }
        )
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        queryset = User.objects.filter(username__iexact=username) 
        
        if username in not_allowed_username:
            raise forms.ValidationError('Invalid Username, try another one')
        
        if queryset.exists():
            raise forms.ValidationError('User already exists, Please Login instead')
        return username
    
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        queryset = User.objects.filter(email__iexact=email)
        
        if queryset.exists():
            return forms.ValidationError('This email already exists, try another one')
        return email
            
            

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'user-password'
            }   # html attributes
        )
    )
    
    # to authenticate and verifiy
    # def clean(self):    
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')


    def clean_username(self):
        username = self.cleaned_data.get('username')
        queryset = User.objects.filter(username__iexact=username) # iextract -> username == username
        
        if not queryset.exists():
            raise forms.ValidationError('This is an Invalid User')
        return username
    
    
# for usename and email
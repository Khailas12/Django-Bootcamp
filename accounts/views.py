from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import LoginForm


def login_view(request, *args,**kwargs):
    form = LoginForm(request.POST or None)
    
    if form.is_valid():
        username = form.cleaned_data('username')
        password = form.cleaned_data('password')
        user = authenticate(request, username=username, password=password)    
        
        if user == None:    # if invalid username or pswd
            # attempt = request.session.get('attempt') or 0
            # request.session['attempt'] = attempt + 1
            request.session['invalid_user'] = 1     # 1=True
            context = {'form': form}
            return render(request, 'products/forms.html', context)
        
        else:   # if valid user
            login(request, user)
            return redirect('/')
    
    context = {'form': form}
    return render(redirect, 'forms.html', context)
    
    
def logout_view(request):
    logout(request)     # request.user == anonymous user
    return redirect('/login')
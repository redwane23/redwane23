from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from .forms import AccountCreationFome
from django.contrib.auth.decorators import login_required

def create_account(request): 
    if request.method == 'POST':
        form = AccountCreationForm(request.POST,request.FILES)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user = authenticate(username=new_user.username, password=form.cleaned_data['password'])
            login(request, user)
            return redirect('')
    else:
        form =  AccountCreationForm()
    return render(request, 'account/creat_account.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'account/login.html'
@login_required
def my_account(request):
    templet_name='account/my_account.html'

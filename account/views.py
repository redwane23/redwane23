from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from .forms import AccountCreationForm
from django.contrib.auth.decorators import login_required

def create_account(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            return redirect('')  # Redirect to the homepage or any other page
    else:
        form = AccountCreationForm()
    return render(request, 'account/creat_account.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'account/login.html'
@login_required
def my_account(request):
    templet_name='account/my_account.html'

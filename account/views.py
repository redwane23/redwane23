from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.backends.base.base import DatabaseWrapper
from asgiref.sync import sync_to_async
from .forms import UserRegistrationForm
from django.urls import reverse

# Helper to handle synchronous operations within async views
database_sync_to_async = sync_to_async

async def create_account(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            await database_sync_to_async(new_user.save)()
            user = await database_sync_to_async(authenticate)(username=new_user.username, password=form.cleaned_data['password'])
            if user is not None:
                await database_sync_to_async(login)(request, user)
                return redirect(reverse('home:index'))  # Use named URL pattern or view name
    else:
        form = UserRegistrationForm()
    return render(request, 'account/create_account.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'account/login.html'

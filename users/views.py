from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .forms import LoginForm, RegistrationForm


def login_page(request):
    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
    context = {'form': forms}
    return render(request, 'users/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data.get('email')
            password = form.cleaned_data['password1']
            
            User = get_user_model()
            # check if username already exists
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists')
                return render(request, 'users/register.html', {'form': form})
            
            # validate password using Django validators
            try:
                validate_password(password)
            except ValidationError as e:
                form.add_error('password1', e)
                return render(request, 'users/register.html', {'form': form})

            # create user as buyer
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_buyer = True
            user.save()
            # don't auto-login; redirect to login page so the user can sign in
            return redirect('login')

    return render(request, 'users/register.html', {'form': form})

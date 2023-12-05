from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.forms.utils import ErrorDict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.defaulttags import url
from django.urls import reverse

from tester_app.forms import NameForm, LoginForm, RegisterForm

context = {
    'login_form': LoginForm(label_suffix=''),
    'has_header': True
}


def index(request):
    global context
    context['title'] = 'Главная'
    context['has_header'] = True
    return render(request, 'tester_app/index.html', context)


def about(request):
    context['title'] = 'О сайте'
    context['has_header'] = True
    return render(request, 'tester_app/about.html', context)


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            if user := form.login():
                login(request, user)
                if user.is_superuser or user.is_staff:
                    print('Is superuser')
                    return redirect('/admin')
                return redirect(reverse('index'))

    messages.error(request, 'Login failed')
    return redirect(reverse('index') + '#login')


def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse('profile'))

    context['title'] = 'Зарегистрироваться'
    context['has_header'] = False

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] != form.cleaned_data['password2']:
                messages.error(request, 'Password mismatch')
            elif User.objects.filter(username=form.cleaned_data['login']):
                messages.error(request, 'Username exists')
            else:
                user = form.register()
                if user:
                    firstname = form.cleaned_data['login']
                    messages.success(request, f"Register <{firstname}> success")
                else: messages.error(request, "Signup failed")

        else:
            messages.error(request, form.errors)

    else:
        form = RegisterForm(label_suffix='')

    context['signup_form'] = form
    return render(request, 'tester_app/signup.html', context)


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


@login_required(login_url='login')
def profile_view(request):
    context['title'] = 'Профиль'
    context['has_header'] = True
    user = request.user
    if user.is_superuser or user.is_staff:
        return redirect(f'/admin/auth/user/{user.id}')
    return render(request, 'tester_app/profile.html', context)


def forms_view(request):
    context['has_header'] = True
    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['your_name']
            messages.success(request, f"Message from <{username}> sent.")
        else:
            messages.error(request, form.errors)

    else:
        form = NameForm()

    context['form_test'] = form
    return render(request, 'tester_app/forms_view.html', context)

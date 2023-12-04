from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.forms.utils import ErrorDict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.defaulttags import url
from django.urls import reverse

from tester_app.forms import NameForm, LoginForm

context = {'form': LoginForm(label_suffix='')}


def index(request):
    global context
    context['title'] = 'Главная'
    return render(request, 'tester_app/index.html', context)


def about(request):
    context['title'] = 'О сайте'
    return render(request, 'tester_app/about.html', context)


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid() :
            if user := form.login():
                if user.is_superuser or user.is_staff:
                    print('Is superuser')
                    return redirect('/admin')
            return redirect(reverse('index'))

    messages.error(request, 'Login failed')
    return redirect(reverse('index') + '#login')


def signup(request):
    context['title'] = 'Зарегистрироваться'
    return render(request, 'tester_app/about.html', context)


def forms_view(request):
    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['your_name']
            messages.success(request, f"Message from <{username}> sent.")
        else:
            messages.error(request, form.errors.as_text())

    else:
        form = NameForm()

    return render(request, 'tester_app/forms_view.html', {"form": form})

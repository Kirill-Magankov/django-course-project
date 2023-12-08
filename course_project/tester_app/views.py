import io
import subprocess
import sys

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.forms.utils import ErrorDict
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaulttags import url
from django.urls import reverse

from tester_app.forms import NameForm, LoginForm, RegisterForm, UpdateUserForm
from tester_app.models import Testing, Answer, Question

context = {
    'login_form': LoginForm(label_suffix=''),
    'has_header': True
}


def index(request):
    testing = Testing.objects.all()
    global context
    context['title'] = 'Главная'
    context['has_header'] = True
    context['data'] = testing
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
                else:
                    messages.error(request, "Signup failed")

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

    form = UpdateUserForm(instance=user)
    context['form'] = form

    answers = ((Answer.objects.filter(user=user).distinct()
                .values('datetime', 'question__test__name'))
               .order_by('-datetime'))
    print(answers)
    context['data'] = answers

    return render(request, 'tester_app/profile.html', context)


@login_required(login_url='login')
def profile_save(request):
    user = request.user
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=user)

    context['form'] = user_form
    return render(request, 'tester_app/profile.html', context)


def code_view(request):
    context['title'] = 'Code execution'
    context['error'] = ''
    context['result'] = ''

    if request.method == 'POST':
        code_block = request.POST.get('code_block')

        try:
            output = subprocess.run(['python3'], input=code_block, capture_output=True, text=True)

            result = output.stdout
            if error := output.stderr:
                context['error'] = error

            if output.stdout == '':
                result = 'Empty response'

            context['result'] = result
        except Exception as e:
            print(e)

        # user_globals = {}
        # user_locals = {}
        # code_block = request.POST.get('code_block')
        # try:
        #     exec(code_block, user_globals, user_locals)
        #     context['result'] = user_locals
        # except Exception as e:
        #     error_message = f"Ошибка выполнения кода: {str(e)}"
        #     print(error_message)

    return render(request, 'tester_app/code.html', context)


@login_required(login_url='login')
def testing_view(request, test_slug):
    context['title'] = 'Тестирование'
    context['has_header'] = True
    testing_data = Testing.objects.get(slug=test_slug)
    questions = testing_data.question_set
    context['data'] = {'test': testing_data,
                       'questions': questions.all}

    if request.method == 'POST':
        params = request.POST
        for p in params:
            if p.isdigit():
                try:
                    question = questions.get(id=p)
                    answer = params[p]
                    a = Answer(answer=answer, question=question, user=request.user)
                    a.save()
                except Exception as e:
                    messages.error(request, e)
        return redirect('index')

    return render(request, 'tester_app/testing.html', context)

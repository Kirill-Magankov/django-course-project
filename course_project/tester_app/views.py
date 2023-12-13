import io
import subprocess
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from tester_app.forms import NameForm, LoginForm, RegisterForm, UpdateUserForm
from tester_app.models import Testing, Answer, Question, Result

context = {
    'login_form': LoginForm(label_suffix=''),
    'has_header': True
}

PER_PAGE = 5


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

    results = Result.objects.filter(user=user).order_by('-datetime')

    paginator = Paginator(results, PER_PAGE)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context['data'] = page_obj

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


def run_code(code, input_data):
    # Запуск процесса Python с блоком кода
    process = subprocess.Popen(['python3', '-c', code],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    # Ввод данных в stdin
    process.stdin.write(input_data.encode('utf-8'))
    process.stdin.close()

    errors = process.stderr.read()

    # Получение вывода из stdout
    output_data = process.stdout.read()

    # Ожидание завершения процесса
    process.wait()
    return output_data.decode('utf-8'), errors.decode('utf-8')


def code_view(request):
    context['title'] = 'Code execution'
    context['error'] = ''
    context['result'] = ''

    if request.method == 'POST':
        code_block = request.POST.get('code_block')
        test_input = request.POST.get('test_input')
        context['data'] = {
            'code_block': code_block,
            'test_input': test_input,
        }

        try:
            output, error = run_code(code_block, test_input)
            result = output

            if error:
                context['error'] = error
            if not output:
                result = 'Empty response'

            context['result'] = result
        except Exception as e:
            print(e)

    return render(request, 'tester_app/code.html', context)


@login_required(login_url='login')
def testing_view(request, test_slug):
    context['title'] = 'Тестирование'
    context['has_header'] = True
    testing_data = Testing.objects.get(slug=test_slug)
    # questions = testing_data.question_set.order_by('?')
    questions = testing_data.question_set.all()

    step = request.GET.get('step')
    if testing_data.type == 'INTERPRETER' and not step:
        return redirect(reverse('testing', args={test_slug}) + '?step=1')

    if testing_data.type == 'INTERPRETER':
        context['error'] = ''
        context['result'] = ''

    if step:
        step = int(step)

        context['question_link'] = {
            'has_link': False if step == questions.count() else True,
            'next_link': reverse('testing', args={test_slug}) + f'?step={step + 1}',
            'enabled': 'disabled'
        }

        if step > questions.count():
            messages.warning(request, 'Question does not exist')
            return redirect(reverse('testing', args={test_slug}) + '?step=1')
        questions = questions[step - 1]
    else:
        questions = questions

    context['data'] = {'test': testing_data,
                       'questions': questions}

    if request.method == 'POST' and testing_data.type == 'TEST':
        params = request.POST
        correct, wrong = 0, 0
        if len(params) > 1:
            r = Result(test=testing_data, user=request.user, correct=correct, wrong=wrong)
            r.save()
            for p in params:
                if p.isdigit():
                    try:
                        question = questions.get(id=p)
                        answer = params[p]
                        a = Answer(answer=answer, question=question, result=r)
                        a.save()
                        if a.is_correct:
                            correct += 1
                        else:
                            wrong += 1
                    except Exception as e:
                        messages.error(request, e)

            try:
                r.correct = correct
                r.wrong = wrong
                r.save()
            except Exception as e:
                messages.error(request, e)

            return redirect('index')
    elif request.method == 'POST' and testing_data.type == 'INTERPRETER':
        code_block = request.POST.get('code_block')
        test_input = request.POST.get('test_input')
        context['data']['code_block'] = code_block
        context['data']['test_input'] = test_input

        try:
            output, error = run_code(code_block, test_input)
            result = output

            if error:
                context['error'] = error
            if not output:
                result = 'Empty response'

            context['result'] = result
            context['question_link']['enabled'] = 'enabled'
            messages.success(request, 'Everything is correct.')
        except Exception as e:
            print(e)

        if not context['question_link']['has_link']:
            print('Last question')

    return render(request, 'tester_app/testing.html', context)

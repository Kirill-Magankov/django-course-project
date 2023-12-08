from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import formset_factory


class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100,
                                widget=forms.TextInput(attrs={"class": "form-control",
                                                              "placeholder": "Enter your name"}))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Логин',
                               widget=forms.TextInput(attrs={"class": "form-control rounded-3",
                                                             "placeholder": "Enter your username"}))
    password = forms.CharField(max_length=100, label='Пароль',
                               widget=forms.PasswordInput(attrs={"class": "form-control rounded-3",
                                                                 "placeholder": "Enter your password"}))

    def login(self):
        data = self.cleaned_data
        user = authenticate(username=data['username'], password=data['password'])
        return user


class RegisterForm(forms.Form):
    lastname = forms.CharField(max_length=100, label='Фамилия',
                               widget=forms.TextInput(attrs={"class": "form-control",
                                                             "placeholder": "Иванов"}))

    firstname = forms.CharField(max_length=100, label='Имя',
                                widget=forms.TextInput(attrs={"class": "form-control",
                                                              "placeholder": "Дмитрий"}))

    login = forms.CharField(max_length=50, label='Имя пользователя',
                            widget=forms.TextInput(attrs={"class": "form-control",
                                                          "placeholder": "ivanov_dmitry"}))

    email = forms.EmailField(max_length=100, label='E-mail*', required=False,
                             widget=forms.EmailInput(attrs={"class": "form-control",
                                                            "placeholder": "user@yandex.ru"}))

    password1 = forms.CharField(max_length=50, min_length=8, label='Пароль',
                                widget=forms.PasswordInput(attrs={"class": "form-control",
                                                                  "placeholder": "Введите пароль"}))

    password2 = forms.CharField(max_length=50, min_length=8, label='Подтвердите пароль',
                                widget=forms.PasswordInput(attrs={"class": "form-control",
                                                                  "placeholder": "Подтвердите пароль"}))

    def register(self):
        data = self.cleaned_data
        user = User.objects.create_user(data['login'], data['email'], data['password1'])
        user.last_name = data['lastname']
        user.first_name = data['firstname']
        user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    last_name = forms.CharField(max_length=100, label='Фамилия',
                                widget=forms.TextInput(attrs={"class": "form-control",
                                                              "placeholder": "Иванов"}))
    first_name = forms.CharField(max_length=100, label='Имя',
                                 widget=forms.TextInput(attrs={"class": "form-control",
                                                               "placeholder": "Дмитрий"}))
    username = forms.CharField(max_length=50, label='Имя пользователя',
                               widget=forms.TextInput(attrs={"class": "form-control",
                                                             "placeholder": "ivanov_dmitry"}))
    email = forms.EmailField(max_length=100, label='E-mail*', required=False,
                             widget=forms.EmailInput(attrs={"class": "form-control",
                                                            "placeholder": "user@yandex.ru"}))

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'username', 'email']

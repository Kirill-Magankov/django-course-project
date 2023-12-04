from django import forms
from django.contrib.auth import authenticate


class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100,
                                widget=forms.TextInput(
                                    attrs={
                                        "class": "form-control",
                                        "placeholder": "Enter your name"
                                    }))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Логин',
                               widget=forms.TextInput(
                                   attrs={"class": "form-control rounded-3",
                                          "placeholder": "Enter your username"})
                               )
    password = forms.CharField(max_length=100, label='Пароль',
                               widget=forms.PasswordInput(
                                   attrs={"class": "form-control rounded-3",
                                          "placeholder": "Enter your password"})
                               )

    def login(self):
        data = self.cleaned_data
        user = authenticate(username=data['username'], password=data['password'])
        return user

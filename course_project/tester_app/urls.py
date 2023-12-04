from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("forms/", views.forms_view, name="forms"),
]

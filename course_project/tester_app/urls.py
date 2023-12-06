from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("profile/logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/save/", views.profile_save, name="profile_save"),
    path("code/", views.code_view, name="code"),
]

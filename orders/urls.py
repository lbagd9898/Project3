from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.logged_in, name="login"),
    path("register", views.register, name="register"),
    path("log_out", views.log_out, name="log_out")
]

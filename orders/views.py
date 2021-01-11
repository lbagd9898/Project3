from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/index.html")
    context = {
        "user": request.user
    }
    return render(request, "orders/welcome.html", context)

def logged_in(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/index.html", {"message": "Invalid Credentials"})

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = RegisterForm()
    return render(response, "orders/register.html", {"form": form})

def log_out(request):
    logout(request)
    return render(request, "orders/index.html", {"message": "Logged out."})

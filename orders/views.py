from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import Pizzas, Toppings, Pasta, Cart

cart = []
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/index.html")
    toppings = Toppings.objects.all()
    pastas = Pasta.objects.all()
    reg_pizzas = Pizzas.objects.filter(dough="Regular")
    sic_pizzas = Pizzas.objects.filter(dough="Sicilian")
    context = {
        "pastas": pastas,
        "toppings": toppings,
        "reg_pizzas": reg_pizzas,
        "sic_pizzas": sic_pizzas,
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

def order_sicilian(request):
    pizza_id = request.POST["sic_pizza"]
    pizza = Pizzas.objects.get(id=pizza_id)
    # toppings1 = request.POST["sic_toppings1"]
    # toppings2 = request.POST["sic_toppings2"]
    # toppings3 = request.POST["sic_toppings3"]
    piz_toppings = pizza.toppings
    if piz_toppings == "1 Topping":
        top_1 = request.POST["sic_toppings1"]
    return HttpResponse(top_1)

def order_pasta(request):
    pasta = request.POST["pasta"]
    pasta_id = Pasta.objects.get(id=pasta)
    pasta_item = pasta_id.pasta
    pasta_price = pasta_id.price
    quantity = int(request.POST["quantity"])
    total_price = pasta_price * quantity
    current_user = request.user
    cart_item = Cart(item=pasta_item, user=current_user, quantity=quantity, total_price=total_price)
    cart_item.save()
    messages.info(request, f"{quantity} {pasta_item} has been added to your cart!")
    return HttpResponseRedirect(reverse("index"))

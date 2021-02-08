from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
import json

import stripe
# This is your real test secret API key.

stripe.api_key = 'sk_test_51IFscQIv6ZB77sTwZCqFqjd2xuO6Ca2Ks3Zm7OOEzVVgQSW4lY0IJ0nFoPOP8n3HmJyIOn3zZrwDEkkS8WlYSS6X00bAF1gAE9'

from .models import Pizzas, Toppings, Pasta, Cart, Sub, Sub_Extras, Salad, Dinner_platter, Order



def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/index.html")
    toppings = Toppings.objects.all()
    pastas = Pasta.objects.all()
    salads = Salad.objects.all()
    sm_din_plat = Dinner_platter.objects.filter(size="Small")
    lg_din_plat = Dinner_platter.objects.filter(size="Large")
    small_subs = Sub.objects.filter(size="Small")
    large_subs = Sub.objects.filter(size="Large")
    reg_pizzas = Pizzas.objects.filter(dough="Regular")
    sic_pizzas = Pizzas.objects.filter(dough="Sicilian")
    context = {
        "small_subs": small_subs,
        "large_subs": large_subs,
        "pastas": pastas,
        "sm_din_plat": sm_din_plat,
        "lg_din_plat": lg_din_plat,
        "toppings": toppings,
        "reg_pizzas": reg_pizzas,
        "sic_pizzas": sic_pizzas,
        "salads": salads,
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

@login_required
def order_sicilian(request):
    pizza_id = request.POST["sic_pizza"]
    pizza = Pizzas.objects.get(id=pizza_id)
    piz_price = pizza.price
    pizza_item = str(pizza.size + " " + pizza.dough + " " + pizza.toppings + " " +  " Pizza(s)")
    piz_toppings = pizza.toppings
    current_user = request.user
    quantity = int(request.POST["quantity"])
    total_price = piz_price * quantity
    if piz_toppings == "Cheese":
        cart_item=Cart(item=pizza_item, user=current_user, quantity=quantity, total_price=total_price)
        cart_item.save()
        messages.info(request, f"{quantity} {pizza_item} has been added to your cart!")
        return HttpResponseRedirect(reverse("index"))
    elif piz_toppings == "1 Topping":
        top_1_id = request.POST["sic_toppings1"]
        top_1 = Toppings.objects.get(id=top_1_id)
        cart_item=Cart(item=pizza_item, user=current_user, quantity=quantity, total_price=total_price)
        cart_item.save()
        cart_item.toppings.add(top_1)
        messages.info(request, f"{quantity} {pizza_item} have been added to your cart!")
        return HttpResponseRedirect(reverse("index"))
    elif piz_toppings == "2 Toppings":
        top_1_id = request.POST["sic_toppings1"]
        top_2_id = request.POST["sic_toppings2"]
        if top_1_id == top_2_id:
            messages.info(request, "Please select 2 DIFFERENT toppings!")
            return HttpResponseRedirect(reverse("index"))
        else:
            toppings = list(Toppings.objects.filter(id__in=[top_1_id, top_2_id]))
            cart_item=Cart(item=pizza_item, user=current_user, quantity=quantity, total_price=total_price)
            cart_item.save()
            for top in toppings:
                cart_item.toppings.add(top)
            messages.info(request, f"{quantity} {pizza_item} have been added to your cart!")
            return HttpResponseRedirect(reverse("index"))
    elif piz_toppings == "3 Toppings":
        top_1_id = request.POST["sic_toppings1"]
        top_2_id = request.POST["sic_toppings2"]
        top_3_id = request.POST["sic_toppings3"]
        if top_1_id == top_2_id or top_2_id == top_3_id or top_1_id == top_3_id:
            messages.info(request, "Please select 3 DIFFERENT toppings!")
            return HttpResponseRedirect(reverse("index"))
        else:
            toppings = list(Toppings.objects.filter(id__in=[top_1_id, top_2_id, top_3_id]))
            cart_item=Cart(item=pizza_item, user=current_user, quantity=quantity, total_price=total_price)
            cart_item.save()
            for top in toppings:
                cart_item.toppings.add(top)
            messages.info(request, f"{quantity} {pizza_item} have been added to your cart!")
            return HttpResponseRedirect(reverse("index"))
    elif piz_toppings == "Special":
        toppings = list(Toppings.objects.filter(Toppings__in=["Pepperoni", "Sausage", "Ham", "Canadian Bacon"]))
        cart_item=Cart(item=pizza_item, user=current_user, quantity=quantity, total_price=total_price)
        cart_item.save()
        for top in toppings:
            cart_item.toppings.add(top)
        messages.info(request, f"{quantity} {pizza_item} have been added to your cart!")
        return HttpResponseRedirect(reverse("index"))

@login_required
def order_pizza(request):
    pizza_id = request.POST["reg_pizza"]
    pizza = Pizzas.objects.get(id=pizza_id)
    piz_price = pizza.price
    pizza_item = str(pizza.size + " " + pizza.dough + " " + pizza.toppings + " " +  " Pizza(s)")
    piz_toppings = pizza.toppings
    current_user = request.user
    quantity = int(request.POST["quantity"])
    total_price = piz_price * quantity
    if piz_toppings == "Cheese":
        cart_item=Cart(item=pizza_item, user=current_user, quantity=quantity, total_price=total_price)
        cart_item.save()
        messages.info(request, f"{quantity} {pizza_item} have been added to your cart!")
        return HttpResponseRedirect(reverse("index"))
    elif piz_toppings == "1 Topping":
        top_1_id = request.POST["reg_toppings1"]
        top_1 = Toppings.objects.get(id=top_1_id)
        cart_item=Cart(item=pizza_item, user=current_user, quantity=quantity, total_price=total_price)
        cart_item.save()
        cart_item.toppings.add(top_1)
        messages.info(request, f"{quantity} {pizza_item} have been added to your cart!")
        return HttpResponseRedirect(reverse("index"))
    elif piz_toppings == "2 Toppings":
        top_1_id = request.POST["reg_toppings1"]
        top_2_id = request.POST["reg_toppings2"]
        if top_1_id == top_2_id:
            messages.info(request, "Please select 2 DIFFERENT toppings!")
            return HttpResponseRedirect(reverse("index"))
        else:
            toppings = list(Toppings.objects.filter(id__in=[top_1_id, top_2_id]))
            cart_item=Cart(item=pizza_item, user=current_user, quantity=quantity, total_price=total_price)
            cart_item.save()
            for top in toppings:
                cart_item.toppings.add(top)
            messages.info(request, f"{quantity} {pizza_item} have been added to your cart!")
            return HttpResponseRedirect(reverse("index"))
    elif piz_toppings == "3 Toppings":
        top_1_id = request.POST["reg_toppings1"]
        top_2_id = request.POST["reg_toppings2"]
        top_3_id = request.POST["reg_toppings3"]
        if top_1_id == top_2_id or top_2_id == top_3_id or top_1_id == top_3_id:
            messages.info(request, "Please select 3 DIFFERENT toppings!")
            return HttpResponseRedirect(reverse("index"))
        else:
            toppings = list(Toppings.objects.filter(id__in=[top_1_id, top_2_id, top_3_id]))
            cart_item=Cart(item=pizza_item, user=current_user, quantity=quantity, total_price=total_price)
            cart_item.save()
            for top in toppings:
                cart_item.toppings.add(top)
            messages.info(request, f"{quantity} {pizza_item} have been added to your cart!")
            return HttpResponseRedirect(reverse("index"))
    elif piz_toppings == "Special":
        toppings = list(Toppings.objects.filter(Toppings__in=["Pepperoni", "Sausage", "Ham", "Canadian Bacon"]))
        cart_item=Cart(item=pizza_item, user=current_user, quantity=quantity, total_price=total_price)
        cart_item.save()
        for top in toppings:
            cart_item.toppings.add(top)
        messages.info(request, f"{quantity} {pizza_item} have been added to your cart!")
        return HttpResponseRedirect(reverse("index"))

#Processes Pasta Order Form and adds info to Cart model
@login_required
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

#Processes Sub order form and adds info to cart
@login_required
def order_subs(request):
    sub_id = request.POST["sub"]
    sub = Sub.objects.get(id=sub_id)
    quantity = int(request.POST["quantity"])
    sub_item = str(sub.size + " " + sub.sub + " " + "Sub")
    total_price = quantity * sub.price
    extras = []
    if request.POST["cheese"] == "yes":
        cheese = Sub_Extras.objects.get(extra="Cheese")
        total_price += cheese.price
        extras.append(cheese)
    if sub.sub == "Steak+Cheese":
        if request.POST["mushrooms"] == "yes":
            mushrooms = Sub_Extras.objects.get(extra="Mushrooms")
            extras.append(mushrooms)
            total_price += mushrooms.price
        if request.POST["green-peppers"] == "yes":
            grnpeps = Sub_Extras.objects.get(extra="Green Peppers")
            extras.append(grnpeps)
            total_price += grnpeps.price
        if request.POST["onions"] == "yes":
            onions = Sub_Extras.objects.get(extra="Onions")
            extras.append(onions)
            total_price += onions.price
    cart_item = Cart(item=sub_item, user=request.user, quantity=quantity, total_price=total_price)
    cart_item.save()
    for extra in extras:
        cart_item.sub_extras.add(extra)
    messages.info(request, f"{quantity} {sub_item}(s) have been added to your cart!")
    return HttpResponseRedirect(reverse("index"))

@login_required
def order_salad(request):
    salad_id = request.POST["salad"]
    salad = Salad.objects.get(id=salad_id)
    quantity = int(request.POST["quantity"])
    total_price = salad.price * quantity
    current_user = request.user
    cart_item = Cart(item=salad.salad, user=current_user, quantity=quantity, total_price=total_price)
    cart_item.save()
    messages.info(request, f"{quantity} {salad.salad}(s) have been added to your cart!")
    return HttpResponseRedirect(reverse("index"))

@login_required
def order_platter(request):
    id = request.POST["dinner_platter"]
    plat = Dinner_platter.objects.get(id=id)
    quantity = int(request.POST["quantity"])
    total_price = plat.price * quantity
    item = str(plat.size + " " + plat.platter + " Platter")
    cart_item = Cart(item=item, user=request.user, quantity=quantity, total_price=total_price)
    cart_item.save()
    messages.info(request, f"{quantity} {item}(s) have been added to your cart!")
    return HttpResponseRedirect(reverse("index"))

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user, placed_order=False)
    total = 0
    for item in cart_items:
        total += item.total_price
    context = {
        "user": request.user,
        "cart_items": cart_items,
        "total": total
    }
    return render(request, "orders/cart.html", context)

@login_required
def delete_item(request, item_id):
    item = Cart.objects.get(pk=item_id)
    item.delete()
    return HttpResponseRedirect(reverse("view_cart"))


@csrf_exempt
def checkout(request):
    data = json.loads(request.body)
    amount = int(data['amount'] * 100)


    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
      'amount': amount,
      'currency': 'usd',
      'quantity': '1',
      'name': 'Your Order'
    }],
    mode='payment',
    success_url=request.build_absolute_uri(reverse('success')) + '?session_id={CHECKOUT_SESSION_ID}',
    cancel_url=request.build_absolute_uri(reverse('payment_declined')),
    )

    return JsonResponse({
    'session_id': session.id,
    'stripe_public_key': 'pk_test_51IFscQIv6ZB77sTwXFD6H7KtJCzP0q35EVNxKNM64ruOAreLZFvhcujmauanJErqTNgjUmHaXe59XZ0wUUKYOK6X00CH2ZiSG6'
    })

@csrf_exempt
def stripe_webhook(request):
    print('WEBHOOK!')
    # You can find your endpoint's secret in your webhook settings
    endpoint_secret = 'whsec_gc28cBLHedPTFKe31NVNDNQPZ6wZCJL2'

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items)

    return HttpResponse(status=200)

@login_required
def success(request):
    items = Cart.objects.filter(user=request.user, placed_order=False)
    if not request.session.get('counter', None):
        request.session['counter'] = 0
        order_number = request.session['counter']
    else:
        order_number = request.session['counter']
    for item in items:
        order_item = Order(number=order_number, cart_item=item)
        order_item.save()
        item.placed_order = True
        item.save()
    request.session['counter'] += 1
    return render(request, "orders/placed_order.html")

def payment_declined(request):
    return render(request, "orders/declined.html")

@user_passes_test(lambda u: u.is_superuser)
def view_orders(request):
    orders = Order.objects.order_by('number').values('number').distinct()
    order_numbers = {}
    for order in orders:
        num = order["number"]
        order_obj = Order.objects.filter(number=num).first()
        user = order_obj.cart_item.user
        order_numbers[num] = user
    context = {
    "orders": order_numbers,
    }
    print(order_numbers)
    return render(request, "orders/orders.html", context)

@user_passes_test(lambda u: u.is_superuser)
def order(request, order):
    order_items = Order.objects.filter(number=order)
    user = order_items[0].cart_item.user
    context = {
    "order": order,
    "order_items": order_items,
    "user": user
    }
    return render(request, 'orders/view_order.html', context)

@user_passes_test(lambda u: u.is_superuser)
def order_completed(request, order):
    order = Order.objects.filter(number=order)
    order.delete()
    return HttpResponseRedirect(reverse("view_orders"))

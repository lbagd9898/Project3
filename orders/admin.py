from django.contrib import admin

from .models import Toppings, Pizzas, Pasta, Cart

#Register your models here
admin.site.register(Toppings)
admin.site.register(Pizzas)
admin.site.register(Pasta)
admin.site.register(Cart)

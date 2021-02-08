from django.contrib import admin

from .models import Toppings, Pizzas, Pasta, Cart, Sub, Sub_Extras, Salad, Dinner_platter, Order

#Register your models here
admin.site.register(Toppings)
admin.site.register(Pizzas)
admin.site.register(Pasta)
admin.site.register(Cart)
admin.site.register(Sub)
admin.site.register(Sub_Extras)
admin.site.register(Salad)
admin.site.register(Dinner_platter)
admin.site.register(Order)

from django.db import models
from django.conf import settings


class Pizzas(models.Model):
    dough = models.CharField(max_length=12)
    size = models.CharField(max_length=12)
    toppings = models.CharField(max_length=15)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.dough} {self.toppings} Pizza {self.size} - ${self.price}"

class Toppings(models.Model):
    Toppings = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.Toppings}"

class Pasta(models.Model):
    pasta = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.pasta} - ${self.price}"

class Cart(models.Model):
    item = models.CharField(max_length=150)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_item")
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.user}: {self.quantity} {self.item} - ${self.total_price}"

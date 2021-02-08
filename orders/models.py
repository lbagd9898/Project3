from django.db import models
from django.conf import settings
from django.contrib.auth.models import User



class Pizzas(models.Model):
    dough = models.CharField(max_length=12)
    size = models.CharField(max_length=12)
    toppings = models.CharField(max_length=15)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.dough} {self.toppings} Pizza {self.size}: ${self.price}"

class Toppings(models.Model):
    Toppings = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.Toppings}"

class Pasta(models.Model):
    pasta = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.pasta}: ${self.price}"

class Sub(models.Model):
    sub = models.CharField(max_length=64)
    size = models.CharField(max_length=64, default = "")
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.size} {self.sub} Sub: ${self.price}"

class Sub_Extras(models.Model):
    extra = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.extra}"

class Salad(models.Model):
    salad = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.salad}: ${self.price}"

class Dinner_platter(models.Model):
    platter = models.CharField(max_length=64)
    size = models.CharField(max_length=12)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.size} {self.platter} Platter: ${self.price}"

class Cart(models.Model):
    item = models.CharField(max_length=150)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    toppings = models.ManyToManyField(Toppings, blank=True, related_name="itemswtoppings")
    sub_extras = models.ManyToManyField(Sub_Extras, blank=True, related_name="extras")
    placed_order = models.BooleanField(default=False)


    def __str__(self):
        if self.toppings.exists():
            top = "w/ " + ', '.join(str(t) for t in self.toppings.all())
        elif self.sub_extras.exists():
            top = "w/" + ', '.join(str(e) for e in self.sub_extras.all())
        else:
            top = ""
        return f"{self.quantity}  x {self.item} {top} - ${self.total_price}"

class Order(models.Model):
    number = models.IntegerField()
    cart_item = models.ForeignKey(Cart, on_delete=models.PROTECT)

    def __str__(self):
        if self.cart_item.toppings.exists():
            top = "; TOPPINGS: " + ' '.join(str(t) for t in self.cart_item.toppings.all())
        elif self.cart_item.sub_extras.exists():
            top = "; EXTRAS: " + " ".join(str(e) for e in self.cart_item.sub_extras.all())
        else:
            top = ""
        return f"#{self.number} {self.cart_item.user} - {self.cart_item.quantity} {self.cart_item.item} {top}; TOTAL - ${self.cart_item.total_price}"

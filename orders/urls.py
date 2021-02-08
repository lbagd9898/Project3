from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.logged_in, name="login"),
    path("register", views.register, name="register"),
    path("log_out", views.log_out, name="log_out"),
    path("order_pasta", views.order_pasta, name="order_pasta"),
    path("order_sicilian", views.order_sicilian, name="order_sicilian"),
    path("order_pizza", views.order_pizza, name="order_pizza"),
    path("order_subs", views.order_subs, name="order_subs"),
    path("order_salad", views.order_salad, name="order_salad"),
    path("order_platter", views.order_platter, name="order_platter"),
    path("view_cart", views.view_cart, name="view_cart"),
    path("<int:item_id>/delete_item", views.delete_item, name="delete_item"),
    path("view_orders", views.view_orders, name="view_orders"),
    path("<int:order>/view_order", views.order, name="order"),
    path('checkout', views.checkout, name="checkout"),
    path("stripe_webhook", views.stripe_webhook, name="stripe_webhook"),
    path('success', views.success, name="success"),
    path('payment_declined', views.payment_declined, name="payment_declined"),
    path('<int:order>/order_completed', views.order_completed, name="order_completed")
]

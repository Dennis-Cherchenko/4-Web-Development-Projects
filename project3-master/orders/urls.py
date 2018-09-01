from django.urls import include, path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.menu, name="index"),
    path("admin/", admin.site.urls),
    path("users/login", views.login_view, name="login"),
    path("users/logout", views.logout_view, name="logout"),
    path("users/index", views.add_to_cart_view, name="add_to_cart"),
    path("orders/cart", views.cart_view, name="cart"),
    path("orders/orders", views.orders_view, name="orders"),
    path("orders/confirmation", views.confirmation_view, name="confirmation"),
    path("orders/orders_manager", views.orders_manager_view, name="orders_manager"),
]


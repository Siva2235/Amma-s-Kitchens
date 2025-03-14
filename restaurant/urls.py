from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/',views.menu,name='menu'),
    path('special/',views.special,name='special'),
    path('payment/',views.payment,name='payment'),
    path("update-cart/", views.update_cart, name="update_cart"),
    path("load-cart/", views.load_cart, name="load_cart"),
    path("remove-from-cart/", views.remove_from_cart, name="remove_from_cart"),
    path('order-success/', views.order_success, name='order_success'),
]

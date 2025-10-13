from django.urls import path, include
from . import views


urlpatterns = [
  path("", views.index, name="index"),
  path("profile/", views.profile, name = "profile"),
  path("add-to-cart/", views.add_to_cart, name="add_to_cart"), 
  path("cart/", views.user_cart, name="cart"),

]

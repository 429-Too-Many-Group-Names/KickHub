from django.urls import path, include
from . import views


urlpatterns = [
  path("", views.index, name="index"),
  path("profile/", views.profile, name = "profile"),
  path("add-to-cart/", views.add_to_cart, name="add_to_cart"), 
  path("cart/", views.user_cart, name="cart"),
  path('cart/decrease/<int:item_id>/', views.decrease_cart_item, name='decrease_cart_item'),
  path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

]

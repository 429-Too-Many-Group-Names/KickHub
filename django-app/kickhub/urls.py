from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views


urlpatterns = [
  path("", views.index, name="index"),
  path("profile/", views.profile, name = "profile"),
  path("add-to-cart/", views.add_to_cart, name="add_to_cart"), 
  path("cart/", views.user_cart, name="cart"),

  # ✅ ADDED
  # path("cart/update/", views.update_cart_item, name="update_cart_item"),
  # path("cart/remove/", views.remove_from_cart, name="remove_from_cart"),
  # path("checkout/summary/", views.order_summary, name="order_summary"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
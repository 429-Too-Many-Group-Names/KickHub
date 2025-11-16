from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.user_cart, name="cart"),
    path("create-checkout-session", views.create_checkout_session, name="checkout"),
    path("items/<slug:slug>/", views.ItemDetailView.as_view(), name="item_detail"),
    path("webhook/stripe/", views.stripe_webhook, name="stripe_webhook"),
    # path('order/success/', views.order_success, name='order_success'),
    path("order/<int:order_id>", views.order_items, name="order_items"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

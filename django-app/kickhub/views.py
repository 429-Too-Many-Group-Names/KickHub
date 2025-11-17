from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from kickhub.models import (
    Item,
    ShoppingCart,
    CartItem,
    Sizes,
    Order,
    OrderItem,
    CustomUser,
)
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
import stripe
import os
from django.conf import settings
import time

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_ENDPOINT_SECRET


def index(request):
    items = Item.objects.all()
    items_with_sizes = []

    for item in items:
        sizes = Sizes.objects.filter(item=item, quantity__gt=0)
        items_with_sizes.append({"item": item, "sizes": sizes})

    context = {
        "page_title": "Welcome!",
        "message": "This is a dynamic message from our Django view.",
        "items": items_with_sizes,
    }
    return render(request, "index.html", context)


def profile(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect("index")
    
    orders = Order.objects.filter(user=user)
    
    
    return render(request, "user-profile.html", {"user": user, "orders": orders,})


def user_cart(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("index")

    cart, created = ShoppingCart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart)

    if request.method == "POST":
        action = request.POST.get("action")
        cart_item_id = request.POST.get("cart_item_id")
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)

        if action == "increment":
            if cart_item.quantity < cart_item.size.quantity:
                cart_item.quantity += 1
                cart_item.save()
            else:
                messages.warning(request, "Not enough stock available.")

        elif action == "decrement":
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

        elif action == "remove":
            cart_item.delete()

        return redirect(request.path)

    return render(
        request, "cart.html", {"user": user, "cart": cart, "cart_items": cart_items}
    )


def add_to_cart(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("index")
    else:
        if request.method == "POST":
            item_id = request.POST.get("item_id")
            size_id = request.POST.get("size_id")
            quantity = int(request.POST.get("quantity", 1))
            item = Item.objects.get(id=item_id)
            size = Sizes.objects.get(id=size_id, item=item)

            if quantity > size.quantity:
                return JsonResponse({"Error": "Not enough stock available"})

            cart, created = ShoppingCart.objects.get_or_create(user=user)

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, item=item, size=size, defaults={"quantity": quantity}
            )
            if not created:
                if cart_item.quantity + quantity > size.quantity:
                    return JsonResponse(
                        {"error": "Not enough stock for this size."}, status=400
                    )

                cart_item.quantity += quantity
                cart_item.save()
                
        return JsonResponse({"success": True, "message": "Added to cart!"})


class ItemDetailView(DetailView):
    model = Item
    template_name = "item_detail.html"
    context_object_name = "item"

    def get_queryset(self):
        return Item.objects.prefetch_related("sizes")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        item = ctx["item"]
        available = [s for s in item.sizes.all() if s.quantity > 0]
        ctx["available_sizes"] = available
        ctx["in_stock"] = bool(available)
        return ctx


def create_checkout_session(request):
    user = request.user

    user_cart = ShoppingCart.objects.get(user=user)

    cart_items = CartItem.objects.filter(cart=user_cart)

    line_items_list = []

    for item in cart_items:
        # print(item.quantity)
        line_items_list.append(
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(item.item.price * 100),
                    "product_data": {
                        "name": f"{item.item.name} - Size {item.size.size}",
                        # 'images': [item.item.image.url] if item.item.image else [],
                    },
                },
                "quantity": item.quantity,  # Move quantity outside of price_data
            }
        )

    try:

        customer = stripe.Customer.create(email=user, metadata={"user_id": user.id})

        checkout_session = stripe.checkout.Session.create(
            customer_email=customer.email,
            payment_method_types=["card"],
            line_items=line_items_list,
            mode="payment",
            success_url="http://localhost:8000/",
            cancel_url="http://localhost:8000/cart",
            metadata={"user_id": user.id, "create_at": int(time.time())},
            automatic_tax={"enabled": True},
        )

        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return JsonResponse({"error": str(e)})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        try:
            user_id = session["metadata"]["user_id"]
            user = CustomUser.objects.get(id=user_id)
            cart = ShoppingCart.objects.get(user=user)
            cart_items = CartItem.objects.filter(cart=cart)
            shipping_address = None
            if "shipping" in session and session["shipping"]:
                shipping_address = session["shipping"]["address"]
            elif "customer_details" in session and session["customer_details"]:
                shipping_address = session["customer_details"]["address"]

            for cart_item in cart_items:
                size = cart_item.size
                size.quantity = max(0, size.quantity - cart_item.quantity)
                size.save()
                
            if shipping_address:
                shipping_address_str = ", ".join(
                    str(shipping_address.get(key, ""))
                    for key in [
                        "line1",
                        "line2",
                        "city",
                        "state",
                        "postal_code",
                        "country",
                    ]
                )
            else:
                shipping_address_str = ""

            order = Order.objects.create(
                user=user,
                stripe_checkout_session_id=session["id"],
                total_amount=(
                    session.get("amount_total", 0) / 100
                    if session.get("amount_total")
                    else 0
                ),
                status="completed",
                shipping_address=shipping_address_str,
            )
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    item=cart_item.item,
                    size=cart_item.size,
                    quantity=cart_item.quantity,
                    price=cart_item.item.price,
                )
            cart.cart_items.all().delete()
            cart.checked_out = True
            print(cart)
            cart.save()
            print(
                "Cart items after delete:", cart.cart_items.count()
            )
        except Exception as e:
            return HttpResponse(status=500)
    return HttpResponse(status=200)


def order_items(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = OrderItem.objects.filter(order=order)
    shipping_list = order.shipping_address.split(',')
    shipping_list.remove(' None')
    shipping_address = ','.join(shipping_list)
    return render(request, "order_items.html", {"order": order, "order_items": items, 'shipping_address': shipping_address})

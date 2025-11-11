from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from kickhub.models import Item, ShoppingCart, CartItem, Sizes
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# ADDED: import for flexible search queries
from django.db.models import Q
# ADDED: for totals on order summary
from decimal import Decimal


# Create your views here.

def index(request):
  # ADDED: read query string (?q=...)
  q = request.GET.get('q', '').strip()

  items = Item.objects.all()

  # ADDED: server-side filtering (retrieve only matching items)
  if q:
    items = items.filter(
      Q(description__icontains=q) |
      Q(brand__icontains=q) |
      Q(model__icontains=q) |
      Q(color__icontains=q)
    )

  items_with_sizes = []
  
  for item in items:
    sizes = Sizes.objects.filter(item=item, quantity__gt=0)
    items_with_sizes.append({
      'item': item,
      'sizes': sizes
    })

    
  context = {
    'page_title': 'Welcome!',
    'message': 'This is a dynamic message from our Django view.',
    'items': items_with_sizes,
    # ADDED: pass q back to template so the input shows current value
    'q': q,
  }
  return render(request, 'index.html', context)


def profile(request):
  user = request.user
  if not request.user.is_authenticated:
    return redirect('index')
  return render(request, 'user-profile.html', {"user": user})

def user_cart(request):
  user = request.user
  if not user.is_authenticated:
    return redirect('index')
  
  cart, created = ShoppingCart.objects.get_or_create(user=user)
  cart_items = CartItem.objects.filter(cart=cart)
  
  return render(request, 'cart.html', {"user": user, "cart": cart, "cart_items": cart_items})
  
  
def add_to_cart(request):
  user = request.user
  if not user.is_authenticated:
    return redirect('index')
  else:
    if request.method == "POST":
      item_id = request.POST.get("item_id")
      quantity = int(request.POST.get("quantity", 1))
      item = Item.objects.get(id=item_id)
      user = request.user


      cart, created = ShoppingCart.objects.get_or_create(user=user)


      cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item, defaults={'quantity': quantity})
      cart_item.quantity += quantity
      cart_item.save()
      

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      return JsonResponse({'success': True, 'message': 'Added to cart!'})
      return redirect(request.META.get('HTTP_REFERER', 'index'))
    else:
      return redirect('index')


# ====== ADDED BELOW: cart helpers, update/remove actions, and order summary ======

def _get_user_cart(user):
  """Helper: get or create the current user's cart."""
  cart, _ = ShoppingCart.objects.get_or_create(user=user)
  return cart


def update_cart_item(request):
  """
  POST only.
  Expects: cart_item_id, action in {'inc','dec'}
  - 'inc' -> quantity +1
  - 'dec' -> quantity -1 (delete if becomes 0)
  """
  user = request.user
  if not user.is_authenticated:
    return redirect('index')

  if request.method == "POST":
    cart_item_id = request.POST.get("cart_item_id")
    action = request.POST.get("action")  # 'inc' or 'dec'
    cart = _get_user_cart(user)
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)

    if action == "inc":
      cart_item.quantity += 1
      cart_item.save()
    elif action == "dec":
      if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
      else:
        cart_item.delete()
    # Unknown actions are ignored silently

  return redirect('cart')


def remove_from_cart(request):
  """
  POST only.
  Expects: cart_item_id
  Deletes the item from the user's cart.
  """
  user = request.user
  if not user.is_authenticated:
    return redirect('index')

  if request.method == "POST":
    cart_item_id = request.POST.get("cart_item_id")
    cart = _get_user_cart(user)
    cart_item = CartItem.objects.filter(id=cart_item_id, cart=cart).first()
    if cart_item:
      cart_item.delete()

  return redirect('cart')


def order_summary(request):
  """
  Simple order review page (no payment yet).
  Shows each line item, subtotal, tax, shipping, and total.
  """
  user = request.user
  if not user.is_authenticated:
    return redirect('index')

  cart = _get_user_cart(user)
  cart_items = CartItem.objects.filter(cart=cart).select_related('item')

  items_data = []
  subtotal = Decimal('0.00')
  for ci in cart_items:
    price = Decimal(str(ci.item.price))
    line_total = price * ci.quantity
    subtotal += line_total
    items_data.append({
      "description": ci.item.description,
      "price": price,
      "quantity": ci.quantity,
      "line_total": line_total
    })

  tax = Decimal('0.00')       # adjust if you have tax rules
  shipping = Decimal('0.00')  # adjust if you have shipping rules
  total = subtotal + tax + shipping

  ctx = {
    "items": items_data,
    "subtotal": subtotal,
    "tax": tax,
    "shipping": shipping,
    "total": total
  }
  return render(request, "order-summary.html", ctx)

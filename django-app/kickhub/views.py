from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from kickhub.models import Item, ShoppingCart, CartItem, Sizes
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Sum, F, DecimalField
from decimal import Decimal
from django.shortcuts import get_object_or_404

# Create your views here.

def index(request):
  items = Item.objects.all()
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

  sub_total = Decimal(sum(cart_item.item.price * cart_item.quantity for cart_item in cart_items))
  if sub_total is None:
    sub_total = Decimal('0.00')

  TAX_RATE = Decimal('0.0825')

  tax = sub_total * TAX_RATE
  total = sub_total + tax

  context = {
    'cart_items': cart_items,
    'subtotal': sub_total,
    'tax': tax,
    'total': total,
  }

  return render(request, 'cart.html', context)

  
  
def add_to_cart(request):
  user = request.user
  if not user.is_authenticated:
    return redirect('index')
  else:
    if request.method == "POST":
      item_id = request.POST.get("item_id")
      quantity = int(request.POST.get("quantity", 1))

      item = get_object_or_404(Item, id=item_id)

      cart, _ = ShoppingCart.objects.get_or_create(user=request.user)

      cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        item=item,
        defaults={'quantity': quantity}
      )

      if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return redirect('user_cart')
      
def decrease_cart_item(request, item_id):
  user = request.user
  if not user.is_authenticated:
    return redirect('index')
  else:
    if request.method == "POST":
      cart = get_object_or_404(ShoppingCart, user=request.user)

      item = get_object_or_404(Item, pk=item_id)

      cart_item = CartItem.objects.filter(cart=cart, item=item).first()

      if cart_item:
        if cart_item.quantity > 1:
          cart_item.quantity -= 1
          cart_item.save()
        else:
          cart_item.delete()

    return redirect('cart')


def remove_from_cart(request, item_id):
  user = request.user
  if not user.is_authenticated:
    return redirect('index')
  else:
    if request.method == "POST":
      cart = get_object_or_404(ShoppingCart, user=request.user)
      item = get_object_or_404(Item, pk=item_id)
      CartItem.objects.filter(cart=cart, item=item).delete()

      return redirect('cart') 

  
      
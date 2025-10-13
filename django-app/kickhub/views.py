from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from kickhub.models import Item, ShoppingCart, CartItem, Sizes
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


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
      
      
  
      
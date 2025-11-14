from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import *

CustomUser = get_user_model()

admin.site.register(CustomUser)
admin.site.register(Item)
admin.site.register(Sizes)
admin.site.register(ShoppingCart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)

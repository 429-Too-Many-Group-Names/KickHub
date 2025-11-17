from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import *

CustomUser = get_user_model()

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ['id','order_created_at', 'user','total_amount' ]

admin.site.register(CustomUser)
admin.site.register(Sizes)
admin.site.register(Item)
admin.site.register(ShoppingCart)
admin.site.register(CartItem)
admin.site.register(OrderItem)
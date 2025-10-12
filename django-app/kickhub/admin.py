from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Item

CustomUser = get_user_model()

admin.site.register(CustomUser)
admin.site.register(Item)

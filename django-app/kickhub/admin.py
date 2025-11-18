from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import *
import stripe
from django.conf import settings

CustomUser = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "order_created_at", "user", "total_amount"]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "percent_off",
        "is_active",
        "stripe_coupon_id",
        "stripe_promo_id",
    )
    readonly_fields = ("stripe_coupon_id", "stripe_promo_id")

    def save_model(self, request, obj, form, change):
        try:
            if not obj.stripe_coupon_id:
                coupon = stripe.Coupon.create(
                    percent_off=float(obj.percent_off),
                    duration="once",
                    name=obj.code,
                )
                obj.stripe_coupon_id = coupon.id

            if not obj.stripe_promo_id:
                promo = stripe.PromotionCode.create(
                    promotion={"type": "coupon", "coupon": coupon.id},
                    code=obj.code,
                    active=obj.is_active,
                )
                obj.stripe_promo_id = promo.id
            else:
                stripe.PromotionCode.modify(
                    obj.stripe_promo_id,
                    active=obj.is_active,
                )

            super().save_model(request, obj, form, change)
        except Exception as e:
            from django.core.exceptions import ValidationError

            raise ValidationError(f"Stripe error: {e}")


class DiscountAdmin(admin.ModelAdmin):
    # ...existing code...
    actions = ["deactivate_promo_code"]

    def deactivate_promo_code(self, request, queryset):
        for obj in queryset:
            if obj.stripe_promo_id:
                try:
                    stripe.PromotionCode.update(
                        obj.stripe_promo_id,
                        active=False,
                    )
                    self.message_user(request, f"Promo code {obj.code} deactivated.")
                except Exception as e:
                    self.message_user(
                        request, f"Error deactivating {obj.code}: {e}", level="error"
                    )

    deactivate_promo_code.short_description = "Deactivate selected Stripe promo codes"


admin.site.register(CustomUser)
admin.site.register(Sizes)
admin.site.register(Item)
admin.site.register(ShoppingCart)
admin.site.register(CartItem)
admin.site.register(OrderItem)

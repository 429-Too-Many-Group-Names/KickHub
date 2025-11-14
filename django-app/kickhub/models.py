from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.urls import reverse
from datetime import date


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=150, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class Item(models.Model):
    description = models.TextField()
    brand = models.CharField(max_length=100, default="Unknown")
    model = models.CharField(max_length=100, default="Unknown")
    price = models.FloatField()  # maybe use decimal instead of float
    color = models.CharField(max_length=100, default="Unknown")
    releaseDate = models.DateField(default=date.today)
    image = models.ImageField(upload_to="item_images/", blank=True, null=True)
    slug = models.SlugField(max_length=220, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = (
                slugify(f"{(self.brand or '').strip()} {(self.model or '').strip()}")
                or slugify((self.description or "")[:50])
                or f"item-{self.pk or ''}"
            )
            self.slug = self._unique_slug(base)
        super().save(*args, **kwargs)

    def _unique_slug(self, base):
        """
        Ensure uniqueness: nike-pegasus, nike-pegasus-2, nike-pegasus-3, ...
        """
        slug = base or "item"
        n = 2
        while Item.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base}-{n}"
            n += 1
        return slug

    def get_absolute_url(self):
        return reverse("shop:item_detail", kwargs={"slug": self.slug})

    @property
    def name(self):
        return f"{self.brand} {self.model}".strip()

    @property
    def price_display(self):
        return f"${self.price:.2f}"  # if DecimalField: f"${self.price}"

    def __str__(self):
        return self.name or f"Item #{self.pk}"


class Sizes(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="sizes")
    size = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.item.brand} {self.item.model} - Size {self.size} ({self.quantity} available)"


class ShoppingCart(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="shopping_cart"
    )
    discount_code = models.CharField(max_length=50, blank=True, null=True)
    checked_out = models.BooleanField(default=False)


class CartItem(models.Model):
    cart = models.ForeignKey(
        ShoppingCart, on_delete=models.CASCADE, related_name="cart_items"
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    size = models.ForeignKey(Sizes, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ("cart", "item")


class Order(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="orders"
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default="pending")
    shipping_address = models.TextField(blank=True, null=True)
    stripe_checkout_session_id = models.CharField(
        max_length=255, blank=True, null=True
    )  # <-- Add this line

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    size = models.ForeignKey(Sizes, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("order", "item", "size")

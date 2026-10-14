from django.conf import settings
from django.db import models

MEETUP = {"MAIN_GATE": "Main Gate", "LIBRARY": "Library Steps", "CANTEEN": "Canteen"}


class Order(models.Model):
    PLACED, SHIPPED, DELIVERED, CANCELLED = "placed", "shipped", "delivered", "cancelled"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    payment_method = models.CharField(max_length=10, choices=[("COD", "Cash at Meetup"), ("ONLINE", "Pay Now")])
    meetup_point = models.CharField(max_length=20, choices=list(MEETUP.items()))
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    pincode = models.CharField(max_length=10)
    status = models.CharField(max_length=10, default=PLACED)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def refresh_status(self):
        """An order moves at the pace of its slowest row."""
        live = [i.status for i in self.items.all() if i.status != "cancelled"]
        if not live:
            self.status = self.CANCELLED
        elif all(s == "delivered" for s in live):
            self.status = self.DELIVERED
            if self.payment_method == "COD":
                self.is_paid = True
        elif any(s in ("shipped", "delivered") for s in live):
            self.status = self.SHIPPED
        else:
            self.status = self.PLACED
        self.save()

    @property
    def can_cancel(self):
        return self.status == self.PLACED and all(i.status == "placed" for i in self.items.all())

    @property
    def total_price(self):
        return sum((i.price * i.quantity for i in self.items.all()), 0)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    listing = models.ForeignKey("listings.Listing", null=True, on_delete=models.SET_NULL)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="sold_items")
    # copied from the listing so old orders never change
    title = models.CharField(max_length=200)
    hostel = models.CharField(max_length=100)
    condition = models.CharField(max_length=20)
    image_url = models.CharField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, default="placed")

    class Meta:
        ordering = ["id"]

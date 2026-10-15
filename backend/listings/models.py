from django.conf import settings
from django.db import models


class Listing(models.Model):
    CATEGORY_CHOICES = [
        ("Books", "Books"),
        ("Electronics", "Electronics"),
        ("Hostel Essentials", "Hostel Essentials"),
        ("Cycles", "Cycles"),
        ("Sports", "Sports"),
    ]
    CATEGORIES = [name for name, _ in CATEGORY_CHOICES]
    CONDITIONS = ["Like New", "Good", "Fair"]

    title = models.CharField(max_length=200)
    hostel = models.CharField(max_length=100)
    condition = models.CharField(max_length=20, choices=[(c, c) for c in CONDITIONS], default="Good")
    negotiable = models.BooleanField(default=False)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    imageUrl = models.URLField(max_length=500, blank=True)
    rating = models.FloatField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    availability = models.CharField(max_length=10, choices=[("Available", "Available"), ("Sold", "Sold")], default="Available")
    description = models.TextField(blank=True)
    is_senior_deal = models.BooleanField(default=False)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return self.title

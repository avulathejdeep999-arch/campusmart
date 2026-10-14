import django_filters
from .models import Listing


class ListingFilter(django_filters.FilterSet):
    rating = django_filters.NumberFilter(field_name="rating", lookup_expr="gte")  # rating=4 means 4 and up

    class Meta:
        model = Listing
        fields = ["category", "hostel", "is_senior_deal", "availability"]

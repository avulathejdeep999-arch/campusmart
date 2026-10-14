from rest_framework import serializers
from .models import Listing


class ListingSerializer(serializers.ModelSerializer):
    """Public shape. Note imageUrl (camelCase) next to snake_case fields - on purpose."""
    class Meta:
        model = Listing
        fields = ["id", "title", "hostel", "condition", "negotiable", "category", "price", "imageUrl",
                  "rating", "total_reviews", "availability", "description", "is_senior_deal", "seller_name"]
        read_only_fields = ["rating", "total_reviews", "seller_name"]
    seller_name = serializers.CharField(source="seller.username", read_only=True)

    def validate_price(self, v):
        if v <= 0:
            raise serializers.ValidationError("Price must be more than zero.")
        return v


class SellerListingSerializer(ListingSerializer):
    """Seller list renames imageUrl -> image_url on the way out."""
    image_url = serializers.CharField(source="imageUrl", read_only=True)

    class Meta(ListingSerializer.Meta):
        fields = [f for f in ListingSerializer.Meta.fields if f != "imageUrl"] + ["image_url"]

from decimal import Decimal
from rest_framework import serializers
from .models import MEETUP, Order, OrderItem


class AddressSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=100)
    phone = serializers.RegexField(r"^\d{10}$", error_messages={"invalid": "Phone must be 10 digits."})
    address = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=80)
    state = serializers.CharField(max_length=80)
    pincode = serializers.RegexField(r"^\d{6}$", error_messages={"invalid": "Pincode must be 6 digits."})


class CheckoutSerializer(serializers.Serializer):
    payment_method = serializers.ChoiceField(choices=["COD", "ONLINE"])
    meetup_point = serializers.ChoiceField(choices=list(MEETUP))
    address = AddressSerializer()


class OrderItemSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "listing", "title", "hostel", "condition", "image_url", "price", "quantity", "amount", "status"]

    def get_amount(self, item):
        return str(item.price * item.quantity)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()
    can_cancel = serializers.BooleanField(read_only=True)
    meetup_point_label = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "created_at", "status", "is_paid", "payment_method", "meetup_point", "meetup_point_label",
                  "address", "total_price", "total_items", "can_cancel", "items"]

    def get_total_price(self, o):
        return str(sum((i.price * i.quantity for i in o.items.all()), Decimal("0.00")))

    def get_total_items(self, o):
        return sum(i.quantity for i in o.items.all())

    def get_meetup_point_label(self, o):
        return MEETUP[o.meetup_point]

    def get_address(self, o):
        return {k: getattr(o, k) for k in ("full_name", "phone", "address", "city", "state", "pincode")}

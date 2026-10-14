from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from .models import Order, OrderItem
from .serializers import CheckoutSerializer, OrderSerializer


class OrderListCreate(generics.ListAPIView):
    serializer_class = OrderSerializer
    filter_backends = []

    def get_queryset(self):  # 14 - only YOUR orders
        return Order.objects.filter(user=self.request.user).prefetch_related("items")

    def post(self, request):  # 15 - checkout. Browser sends NO cart and NO total.
        s = CheckoutSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        cart = Cart.objects.filter(user=request.user).first()
        rows = list(cart.items.select_related("listing", "listing__seller")) if cart else []
        if not rows:
            return Response({"detail": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)
        a = s.validated_data["address"]
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user, payment_method=s.validated_data["payment_method"],
                meetup_point=s.validated_data["meetup_point"],
                is_paid=s.validated_data["payment_method"] == "ONLINE", **a)
            for r in rows:  # copy the listing so the order keeps the price actually paid
                l = r.listing
                OrderItem.objects.create(order=order, listing=l, seller=l.seller, title=l.title, hostel=l.hostel,
                                         condition=l.condition, image_url=l.imageUrl, price=l.price, quantity=r.quantity)
            cart.items.all().delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderDetail(generics.RetrieveAPIView):  # 16
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)  # someone else's id -> 404


class OrderCancel(APIView):  # 17
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        if not order.can_cancel:
            return Response({"detail": "This order can no longer be cancelled."}, status=400)
        order.items.update(status="cancelled")
        order.refresh_status()
        return Response(OrderSerializer(order).data)

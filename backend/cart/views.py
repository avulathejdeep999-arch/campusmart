from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from listings.models import Listing
from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer


def get_cart(user):
    return Cart.objects.get_or_create(user=user)[0]


class CartView(APIView):
    def get(self, request):
        return Response(CartSerializer(get_cart(request.user)).data)


class CartAddView(APIView):
    def post(self, request):
        listing = get_object_or_404(Listing, pk=request.data.get("listing"))
        try:
            qty = int(request.data.get("quantity", 1))
        except (TypeError, ValueError):
            qty = 0
        if qty < 1:
            return Response({"detail": "Quantity must be at least 1."}, status=400)
        if listing.availability != "Available":
            return Response({"detail": "This listing is already sold."}, status=400)
        item, created = CartItem.objects.get_or_create(cart=get_cart(request.user), listing=listing, defaults={"quantity": qty})
        if not created:
            item.quantity += qty
            item.save()
        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)


class CartItemView(APIView):
    def _item(self, request, pk):
        return get_object_or_404(CartItem, pk=pk, cart__user=request.user)  # someone else's row -> 404

    def patch(self, request, pk):
        item = self._item(request, pk)
        try:
            qty = int(request.data.get("quantity"))
        except (TypeError, ValueError):
            qty = 0
        if qty < 1:
            return Response({"detail": "Quantity must be at least 1."}, status=400)
        item.quantity = qty  # SETS the quantity, does not add
        item.save()
        return Response(CartItemSerializer(item).data)

    def delete(self, request, pk):
        self._item(request, pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

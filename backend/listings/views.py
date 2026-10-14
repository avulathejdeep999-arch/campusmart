from rest_framework import generics, permissions
from rest_framework.exceptions import NotAuthenticated, PermissionDenied

from .filters import ListingFilter
from .models import Listing
from .permissions import IsSeller, visible_listings
from .serializers import ListingSerializer


def truthy(v):
    return str(v).lower() in ("true", "1", "yes")


class ListingListCreate(generics.ListCreateAPIView):
    serializer_class = ListingSerializer
    filterset_class = ListingFilter
    search_fields = ["title", "hostel"]
    ordering_fields = ["price", "rating", "id"]
    ordering = ["id"]

    def get_permissions(self):
        return [IsSeller()] if self.request.method == "POST" else [permissions.AllowAny()]

    def get_queryset(self):  # runs on EVERY request, so it knows who is asking
        if truthy(self.request.query_params.get("is_senior_deal")) and not self.request.user.is_authenticated:
            raise NotAuthenticated("Log in to see Senior-Only Deals.")
        return visible_listings(self.request.user, Listing.objects.select_related("seller"))

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)  # owner comes from the token, never from React


class ListingDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.select_related("seller")

    def get_permissions(self):
        return [permissions.AllowAny()] if self.request.method == "GET" else [IsSeller()]

    def get_object(self):
        obj = super().get_object()
        if obj.is_senior_deal and not self.request.user.is_authenticated:
            raise NotAuthenticated("Log in to see Senior-Only Deals.")
        if self.request.method != "GET" and obj.seller_id != self.request.user.id:
            raise PermissionDenied("You can only change your own listings.")
        return obj

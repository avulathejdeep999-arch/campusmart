from datetime import timedelta
from decimal import Decimal

from django.db.models import Count, F, Sum
from django.db.models.functions import TruncDate
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from listings.models import Listing
from listings.permissions import IsSeller
from listings.serializers import SellerListingSerializer
from orders.models import OrderItem

NEXT = {"placed": "shipped", "shipped": "delivered"}


class SellerListings(generics.ListAPIView):  # 18
    permission_classes = [IsSeller]
    serializer_class = SellerListingSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title"]

    def get_queryset(self):
        return Listing.objects.filter(seller=self.request.user).select_related("seller").order_by("-id")


def item_json(i):
    return {"id": i.id, "order": i.order_id, "listing": i.listing_id, "title": i.title, "quantity": i.quantity,
            "price": str(i.price), "amount": str(i.price * i.quantity), "status": i.status,
            "buyer": i.order.user.username, "meetup_point": i.order.get_meetup_point_display(),
            "created_at": i.order.created_at}


class SellerOrders(generics.ListAPIView):  # 19
    permission_classes = [IsSeller]
    filter_backends = []

    def get_queryset(self):
        return OrderItem.objects.filter(seller=self.request.user).select_related("order", "order__user").order_by("-id")

    def list(self, request, *a, **kw):
        page = self.paginate_queryset(self.get_queryset())
        return self.get_paginated_response([item_json(i) for i in page])


class SellerOrderAdvance(APIView):  # 20 - moves a row forward: placed -> shipped -> delivered
    permission_classes = [IsSeller]

    def patch(self, request, pk):
        item = get_object_or_404(OrderItem.objects.select_related("order", "order__user"), pk=pk, seller=request.user)
        nxt = NEXT.get(item.status)
        if not nxt:
            return Response({"detail": f"A {item.status} row cannot move forward."}, status=400)
        item.status = nxt
        item.save()
        item.order.refresh_status()
        return Response(item_json(item))


class SellerDashboard(APIView):  # 21
    permission_classes = [IsSeller]

    def get(self, request):
        items = OrderItem.objects.filter(seller=request.user)
        live = items.exclude(status="cancelled")
        money = lambda v: str(v or Decimal("0.00"))
        revenue = live.aggregate(t=Sum(F("price") * F("quantity")))["t"]
        today = timezone.now().date()
        per_day = {r["d"]: r for r in live.annotate(d=TruncDate("order__created_at")).values("d")
                   .annotate(rev=Sum(F("price") * F("quantity")), n=Sum("quantity"))}
        chart = []
        for k in range(6, -1, -1):  # always seven bars, even empty days
            d = today - timedelta(days=k)
            r = per_day.get(d)
            chart.append({"date": d.isoformat(), "revenue": money(r["rev"] if r else None), "items": r["n"] if r else 0})
        top = live.values("title").annotate(qty=Sum("quantity"), rev=Sum(F("price") * F("quantity"))).order_by("-rev")[:5]
        by_status = {s: 0 for s in ("placed", "shipped", "delivered", "cancelled")}
        for r in items.values("status").annotate(n=Count("id")):
            by_status[r["status"]] = r["n"]
        return Response({
            "total_listings": Listing.objects.filter(seller=request.user).count(),
            "total_orders": live.values("order").distinct().count(),
            "items_sold": live.aggregate(t=Sum("quantity"))["t"] or 0,
            "revenue": money(revenue),
            "to_hand_over": by_status["placed"] + by_status["shipped"],
            "last_7_days": chart,
            "top_listings": [{"title": t["title"], "quantity": t["qty"], "revenue": str(t["rev"])} for t in top],
            "items_by_status": by_status,
        })

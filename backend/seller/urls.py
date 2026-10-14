from django.urls import path
from .views import SellerDashboard, SellerListings, SellerOrderAdvance, SellerOrders

urlpatterns = [
    path("listings/", SellerListings.as_view()),                      # 18
    path("orders/", SellerOrders.as_view()),                          # 19
    path("orders/<int:pk>/advance/", SellerOrderAdvance.as_view()),   # 20
    path("dashboard/", SellerDashboard.as_view()),                    # 21
]

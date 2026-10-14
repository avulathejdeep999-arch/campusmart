from django.urls import path
from .views import ListingDetail, ListingListCreate

urlpatterns = [
    path("", ListingListCreate.as_view()),       # 5 (GET) and 6 (POST)
    path("<int:pk>/", ListingDetail.as_view()),  # 7 (GET), 8 (PATCH), 9 (DELETE)
]

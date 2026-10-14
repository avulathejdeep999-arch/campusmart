from django.urls import path
from .views import OrderCancel, OrderDetail, OrderListCreate

urlpatterns = [
    path("", OrderListCreate.as_view()),               # 14 (GET), 15 (POST)
    path("<int:pk>/", OrderDetail.as_view()),          # 16
    path("<int:pk>/cancel/", OrderCancel.as_view()),   # 17
]

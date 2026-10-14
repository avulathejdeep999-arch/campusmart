from django.urls import path
from .views import CartAddView, CartItemView, CartView

urlpatterns = [
    path("", CartView.as_view()),                    # 10
    path("add/", CartAddView.as_view()),             # 11
    path("items/<int:pk>/", CartItemView.as_view()), # 12 (PATCH), 13 (DELETE)
]

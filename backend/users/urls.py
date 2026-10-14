from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LogoutView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view()),          # 1
    path("login/", TokenObtainPairView.as_view()),      # 2
    path("logout/", LogoutView.as_view()),              # 3
    path("token/refresh/", TokenRefreshView.as_view()), # 4
]

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    STUDENT, SELLER = "student", "seller"
    user_type = models.CharField(max_length=10, choices=[(STUDENT, "Student"), (SELLER, "Seller")], default=STUDENT)

from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "password", "user_type"]
        extra_kwargs = {"email": {"required": False}, "user_type": {"required": False}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

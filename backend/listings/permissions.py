from rest_framework import permissions


def visible_listings(user, queryset):
    """The ONE place that decides who sees what. Visitors never get senior-only deals."""
    if user and user.is_authenticated:
        return queryset
    return queryset.filter(is_senior_deal=False)


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        u = request.user
        return bool(u and u.is_authenticated and u.user_type == "seller")

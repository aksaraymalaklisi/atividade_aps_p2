from rest_framework import permissions

from apps.organizations.domain.value_objects import MembershipRole
from apps.organizations.models import Membership


class IsOrganizationOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an organization to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        try:
            membership = Membership.objects.get(user=request.user, organization=obj)
            return membership.role == MembershipRole.OWNER.value
        except Membership.DoesNotExist:
            return False


class IsOrganizationLeaderOrOwner(permissions.BasePermission):
    """
    Custom permission to allow leaders and owners to manage members.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        try:
            membership = Membership.objects.get(user=request.user, organization=obj)
            return membership.role in [MembershipRole.OWNER.value, MembershipRole.LEADER.value]
        except Membership.DoesNotExist:
            return False


class IsOrganizationMember(permissions.BasePermission):
    """
    Custom permission to allow any member to view organization details.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        return Membership.objects.filter(user=request.user, organization=obj).exists()


class IsOperator(permissions.BasePermission):
    """
    Operator role permission. Assuming operators are superusers or staff for now,
    or have a specific flag. We'll use is_staff for simplicity in this exercise.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

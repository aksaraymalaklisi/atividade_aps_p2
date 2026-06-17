from rest_framework import permissions


class IsPublicationOwnerOrOrgMember(permissions.BasePermission):
    """
    Object-level permission to only allow owners of the publication or
    members of the associated organization to edit/delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        # If user is the direct publisher
        if obj.publisher_id == request.user.id:
            return True

        # If publication belongs to an organization, check if user is a member
        if obj.organization_id:
            # We assume request.user.memberships.filter exists (from organizations models)
            return request.user.memberships.filter(organization_id=obj.organization_id).exists()

        return False

from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission class to allow only the owner of the object to modify it.
    Grants permission:
    - Read-only access ('GET', 'HEAD' ,'OPTIONS') to everyone.
    - Write access ('PUT', 'PATCH', 'DELETE') only to the owner of the object.
    """
    def has_object_permission(self, request, view, obj):
        """
        Determine if the user has permissin to access or modify the object.

        Args:
        request - The HTTP request object.
        view - The view that is handling the request.
        obj - The model instance being accessed.

        Returns, True if the user has permission, false otherwise.
        """

        #allow read-only methods for everyone
        if request.method in ['GET', 'HEAD','OPTIONS']:
            return True
        
        # allow write permissions only if the requesting user requesting is the author of the object
        return obj.author ==request.user
        
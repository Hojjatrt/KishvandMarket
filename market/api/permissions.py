from rest_framework import permissions, exceptions


class IsClient(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            token = request.META.get('HTTP_CLIENT', b'')  # get the request header
            if not token:  # no token passed in request headers
                return False  # authentication did not succeed

            try:
                if token == "1234":  # authentication successful
                    return True
            except:
                raise exceptions.AuthenticationFailed('No such client')  # raise exception if user does not exist

        # Write permissions are only allowed to the owner of the snippet.
        return False

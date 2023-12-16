from rest_framework_simplejwt.tokens import AccessToken
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.exceptions import TokenError
from django.http import JsonResponse

class MeMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        This middleware intercepts certain view requests, particularly those involving user profiles,
        and replaces the "me" keyword with the requesting user"s unique UUID.
        """

        # Target specific viewsets for the middleware application
        target_viewsets = ["ProfilesViewSet"]
        if hasattr(view_func, "cls") and view_func.cls.__name__ in target_viewsets:
            # Retrieve the Authorization header
            auth_header = request.headers.get("Authorization")

            if auth_header:
                try:
                    # Separate the JWT token and decode it
                    token = auth_header.split(" ")[1]
                    token_payload = AccessToken(token).payload

                    # Extract the user_id from the token payload
                    user_id = token_payload["user_id"]

                    # Replace "me" in keyword arguments with user_id
                    if view_kwargs:
                        first_kwarg = next(iter(view_kwargs))
                        if str(view_kwargs[first_kwarg]).lower() == "me":
                            view_kwargs[first_kwarg] = str(user_id)

                except TokenError as te:
                    # Ignore TokenError, but could be extended for specific error handling
                    return JsonResponse({"detail": f"Token is invalid: {te} "}, status=401)

                except IndexError as ie:
                    # Return an error response for invalid or expired tokens
                    return JsonResponse({"detail": f"Token is invalid or expired: {ie}"}, status=401)

        # Proceed to the next middleware or view function
        return None
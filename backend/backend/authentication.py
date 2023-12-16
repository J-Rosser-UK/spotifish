from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.backends import ModelBackend
from rest_framework import authentication, HTTP_HEADER_ENCODING
from rest_framework.request import Request
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token

from administration.models import Account

import uuid
from typing import Optional, Tuple, TypeVar

# Configuring the authentication header types
AUTH_HEADER_TYPES = tuple(api_settings.AUTH_HEADER_TYPES)
AUTH_HEADER_TYPE_ENCODED = {header_type.encode(HTTP_HEADER_ENCODING) for header_type in AUTH_HEADER_TYPES}

# Define a type for User which can either be a Django user or a TokenUser
UserType = TypeVar("UserType", AbstractBaseUser, TokenUser)


class User:
    """ A minimal User class that holds a profile_id attribute. """
    profile_id = None



class JWTAuthentication(authentication.BaseAuthentication):
    """ Authentication plugin that authenticates requests JWT in request header. """

    www_authenticate_realm = "api"
    media_type = "application/json"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def authenticate(self, request: Request) -> Optional[Tuple[UserType, Token]]:
        """
        Authenticates the request by validating the JWT in the header.
        Returns the user and validated token if successful, None otherwise.
        """
        auth_header = self.extract_header(request)
        if not auth_header:
            return None

        token = self.extract_token(auth_header)
        if not token:
            return None

        validated_token = self.get_validated_token(token)
        if not validated_token:
            return None

        return self.get_user(validated_token), validated_token

    def authenticate_header(self, request: Request) -> str:
        """
        Returns the WWW-Authenticate header for 401 Unauthenticated responses.
        """
        return f'{AUTH_HEADER_TYPES[0]} realm="{self.www_authenticate_realm}"'

    def extract_header(self, request: Request) -> Optional[bytes]:
        """
        Extracts and returns the JWT header from the request.
        """
        auth_header = request.META.get(api_settings.AUTH_HEADER_NAME)
        return auth_header.encode(HTTP_HEADER_ENCODING) if isinstance(auth_header, str) else auth_header

    def extract_token(self, header: bytes) -> Optional[bytes]:
        """
        Extracts the JWT from the provided header.
        """
        parts = header.split()
        if not parts or parts[0] not in AUTH_HEADER_TYPE_ENCODED or len(parts) != 2:
            raise AuthenticationFailed(_("Invalid Authorisation header format"), code="bad_authorisation_header")
        return parts[1]

    def get_validated_token(self, raw_token: bytes) -> Token:
        """
        Validates the JWT and returns a Token instance.
        """
        errors = []
        for AuthTokenClass in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthTokenClass(raw_token)
            except TokenError as e:
                errors.append({"token_class": AuthTokenClass.__name__, "token_type": AuthTokenClass.token_type, "message": e.args[0]})
        raise InvalidToken({"detail": _("Token not valid for any token type"), "errors": errors})

    def get_user(self, validated_token: Token) -> UserType:
        """
        Retrieves the user associated with the validated token.
        """
        user_id = validated_token.get(api_settings.USER_ID_CLAIM)
        if not user_id:
            raise InvalidToken(_("No user ID in token"))
        
        user = UserType()
        user.profile_id = uuid.UUID(user_id)
        return user


class JWTStatelessUserAuthentication(JWTAuthentication):
    """
    Implementation of a stateless authentication mechanism using JSON Web Tokens (JWT).
    Stateless authentication avoids server-side storage of user session data, as the JWT contains all necessary information.
    This can improve performance in high-traffic systems. The module also handles custom claims in the JWT.
    """

    def get_user(self, validated_token: Token) -> UserType:
        """
        Retrieves and returns a stateless user object based on the provided validated token.
        Raises InvalidToken if the token lacks a recognizable user identifier.
        """
        user_id_claim = api_settings.USER_ID_CLAIM
        if user_id_claim not in validated_token:
            raise InvalidToken(_("Token lacks a recognisable user identifier"))

        # Retrieve the profile_id from the token
        profile_id = validated_token.get(user_id_claim)
        
        # Create a User instance with the profile_id
        user = User()
        user.profile_id = uuid.UUID(profile_id)

        return user



class EmailUsernameAuthBackend(ModelBackend):
    """ This backend provides authentication using either an email or a username. """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # Determine if the username is an email
        user = None
        if "@" in username:
            user = Account.objects.filter(email=username).first()
        else:
            user = Account.objects.filter(username=username).first()

        # Verify the user and password match
        if user and user.check_password(password):
            return user
        return None



def default_user_authentication_rule(user: UserType) -> bool:
    """
    Determines if a user is active. This function aligns with Django's authentication
    policies post-1.10, which prevent inactive users from authenticating. It ensures 
    backward compatibility and enforces a policy of disallowing inactive user authentication.
    
    Returns True if the user is not None and is marked as active, False otherwise.
    """
    return user is not None and user.is_active
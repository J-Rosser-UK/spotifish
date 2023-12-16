from django.contrib.auth.backends import ModelBackend
from .models import Account

from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import uuid
from django.contrib.auth.views import LoginView

from .serializers import AccountSerializer
from backend.settings import SECRET_KEY
import jwt

from base.models import Profiles
from django.shortcuts import get_object_or_404
from .signup_factory import SignUpFactory

class SignUpView(APIView):
    """
    Handles the creation of new users.
    Accepts user details, validates them, saves the user, and creates an associated profile.
    """

    permission_classes = [permissions.AllowAny]

    @transaction.atomic
    def post(self, request):
        
        # Check missing fields
        required_fields = ['email', 'username', 'password']
        missing_fields = [field for field in required_fields if field not in request.data]

        if missing_fields:
            error_message = f"Missing required fields: {', '.join(missing_fields)}."
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

        # Validate password
        try:
            validate_password(request.data['password'], user=request.data)
        except ValidationError as e:
            validation_errors_list = [error for sublist in e.args[0] for error in sublist]
            return Response({'error': validation_errors_list}, status=status.HTTP_400_BAD_REQUEST)
        
        
        

        # Validate fields
        user_serializer = AccountSerializer(data=request.data)

        if user_serializer.is_valid():
            # Ensure user hasn't already been created
            try:
                user = user_serializer.save()
            except IntegrityError as e:
                return Response({'error': str(e)}, status=status.HTTP_409_CONFLICT)

            if user:
                
                request.data["profile_id"] = user.profile_id
                signup_factory = SignUpFactory(request)

                profile = signup_factory.create()
    
                return Response(request.data, status=status.HTTP_201_CREATED)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogInView(LoginView):
    """
    Enhanced version of the default LoginView to include the user's profile_id in the response.
    """

    def post(self, request, *args, **kwargs):

        response = super().post(request, *args, **kwargs)

        # Extracting the access token
        access_token = response.data.get('access_token')
        if access_token:
            # Decode the JWT token
            user_id = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])['user_id']

            # Incorporate user and profile IDs into the response
            response.data.update({
                'user_id': user_id,
                'profile_id': user_id
            })

            # Retrieve user's profile, return 404 if doesn't exist
            profile = get_object_or_404(Profiles, profile_id = user_id)

        return response
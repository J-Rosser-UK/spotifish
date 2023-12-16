from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    """
    Defines the serializer for Account, inheriting from ModelSerializer.
    """

    email = serializers.EmailField(required=True)  
    username = serializers.CharField(max_length=30, min_length=1)  
    password = serializers.CharField(min_length=8, write_only=True)  # Ensure password is write-only

    class Meta:
        model = Account
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Ensure password is write-only

    def create(self, validated_data):
        """
        Handles the creation of a new Account instance.
        """

        # Ensure that password is provided
        if 'password' not in validated_data:
            raise serializers.ValidationError({"password": "Password is required."})

        # Retrieve password
        password = validated_data.pop('password', None)

        # Create an Account instance
        account_instance = Account(**validated_data)
        account_instance.set_password(password)
        account_instance.save()

        return account_instance

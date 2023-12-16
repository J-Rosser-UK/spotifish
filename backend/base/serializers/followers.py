from rest_framework import serializers
from base.models import FollowersByProfile, FollowingByProfile, Profiles
from django.utils import timezone

class FollowersByProfileSerializer(serializers.Serializer):
    
    profile_id = serializers.UUIDField(source='profile.profile_id', read_only=True)
    profile_type = serializers.CharField(source='profile.profile_type', read_only=True)
    profile_privacy = serializers.CharField(source='profile.profile_privacy', read_only=True)
    profile_name = serializers.CharField(source='profile.profile_name', read_only=True)
    profile_handle = serializers.CharField(source='profile.profile_handle', read_only=True)
    profile_picture = serializers.CharField(source='profile.profile_picture', read_only=True)

    follower_profile_id = serializers.UUIDField(source='follower_profile.profile_id', read_only=True)
    follower_profile_type = serializers.CharField(source='follower_profile.profile_type', read_only=True)
    follower_profile_privacy = serializers.CharField(source='follower_profile.profile_privacy', read_only=True)
    follower_profile_name = serializers.CharField(source='follower_profile.profile_name', read_only=True)
    follower_profile_handle = serializers.CharField(source='follower_profile.profile_handle', read_only=True)
    follower_profile_picture = serializers.CharField(source='follower_profile.profile_picture', read_only=True)
    
    follower_type = serializers.CharField()
    follower_timestamp = serializers.DateTimeField(required=False, allow_null=True, default=timezone.now)

    class Meta:
        model = FollowersByProfile

 
    
class FollowingByProfileSerializer(serializers.Serializer):
    
    profile_id = serializers.UUIDField(source='profile.profile_id', read_only=True)
    profile_type = serializers.CharField(source='profile.profile_type', read_only=True)
    profile_privacy = serializers.CharField(source='profile.profile_privacy', read_only=True)
    profile_name = serializers.CharField(source='profile.profile_name', read_only=True)
    profile_handle = serializers.CharField(source='profile.profile_handle', read_only=True)
    profile_picture = serializers.CharField(source='profile.profile_picture', read_only=True)
    
    following_profile_id = serializers.UUIDField(source='following_profile.profile_id', read_only=True)
    following_profile_type = serializers.CharField(source='following_profile.profile_type', read_only=True)
    following_profile_privacy = serializers.CharField(source='following_profile.profile_privacy', read_only=True)
    following_profile_name = serializers.CharField(source='following_profile.profile_name', read_only=True)
    following_profile_handle = serializers.CharField(source='following_profile.profile_handle', read_only=True)
    following_profile_picture = serializers.CharField(source='following_profile.profile_picture', read_only=True)

    following_timestamp = serializers.DateTimeField(required=False, allow_null=True, default=timezone.now)

    class Meta:
        model = FollowingByProfile



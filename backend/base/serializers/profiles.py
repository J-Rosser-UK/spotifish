from rest_framework import serializers
from base.models import Profiles
from django.utils import timezone

class ProfilesSerializer(serializers.Serializer):
    profile_id = serializers.UUIDField()
    profile_type = serializers.CharField()
    profile_privacy = serializers.CharField()
    profile_name = serializers.CharField(required=False, allow_null=True)
    profile_handle = serializers.CharField()
    profile_picture = serializers.CharField(required=False, allow_null=True)
    profile_links = serializers.JSONField(required=False, allow_null=True)
    profile_upload_timestamp = serializers.DateTimeField(required=False, allow_null=True, default=timezone.now)
    profile_upload_source = serializers.CharField(required=False, allow_null=True)
    profile_followers_counter = serializers.IntegerField(default=0)
    profile_following_counter = serializers.IntegerField(default=0)
    profile_requests_counter = serializers.IntegerField(required=False, allow_null=True)
    profile_superuser_list = serializers.ListField(
        child=serializers.UUIDField(), required=False, default=list
    )
    profile_verification = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Profiles





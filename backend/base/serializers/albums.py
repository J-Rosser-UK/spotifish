from rest_framework import serializers
from base.models import Albums, Profiles
from django.utils import timezone

class AlbumsSerializer(serializers.Serializer):

    profile_id = serializers.UUIDField(source='profile.profile_id', read_only=True)
    profile_type = serializers.CharField(source='profile.profile_type', read_only=True)
    profile_privacy = serializers.CharField(source='profile.profile_privacy', read_only=True)
    profile_name = serializers.CharField(source='profile.profile_name', read_only=True)
    profile_handle = serializers.CharField(source='profile.profile_handle', read_only=True)
    profile_picture = serializers.CharField(source='profile.profile_picture', read_only=True)
    

    album_id = serializers.UUIDField()
    album_original_id = serializers.CharField(required=False, allow_null=True)
    album_name = serializers.CharField()
    album_banner = serializers.CharField(required=False, allow_null=True)
    album_release_date = serializers.DateTimeField(required=False, allow_null=True, default=timezone.now)
    album_links = serializers.JSONField(required=False, allow_null=True)
    album_upload_timestamp = serializers.DateTimeField(required=False, allow_null=True, default=timezone.now)
    album_upload_source = serializers.CharField(required=False, allow_null=True)
    album_likes_counter = serializers.IntegerField(default=0)
    album_tracks_counter = serializers.IntegerField(default=0)
    

    class Meta:
        model = Albums


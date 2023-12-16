from rest_framework import serializers
from base.models import Playlists, PlaylistsByProfile, Profiles
from django.utils import timezone

class PlaylistsSerializer(serializers.Serializer):
    playlist_id = serializers.UUIDField()
    playlist_original_id = serializers.CharField(required=False, allow_null=True)
    playlist_name = serializers.CharField()
    playlist_genre = serializers.CharField(required=False, allow_null=True)
    playlist_subgenre = serializers.CharField(required=False, allow_null=True)
    playlist_privacy = serializers.CharField()
    playlist_banner = serializers.CharField(required=False, allow_null=True)
    playlist_description = serializers.CharField(required=False, allow_null=True)
    playlist_links = serializers.JSONField(required=False, allow_null=True)
    playlist_upload_timestamp = serializers.DateTimeField(required=False, allow_null=True, default=timezone.now)
    playlist_upload_source = serializers.CharField(required=False, allow_null=True)
    playlist_likes_counter = serializers.IntegerField(default=0)
    playlist_tracks_counter = serializers.IntegerField(default=0)
    playlist_admin_list = serializers.ListField(
        child=serializers.UUIDField(), required=False, default=list
    )

    class Meta:
        model = Playlists
   

class PlaylistsByProfileSerializer(serializers.Serializer):

    profile_id = serializers.UUIDField(source='profile.profile_id', read_only=True)
    profile_type = serializers.CharField(source='profile.profile_type', read_only=True)
    profile_privacy = serializers.CharField(source='profile.profile_privacy', read_only=True)
    profile_name = serializers.CharField(source='profile.profile_name', read_only=True)
    profile_handle = serializers.CharField(source='profile.profile_handle', read_only=True)
    profile_picture = serializers.CharField(source='profile.profile_picture', read_only=True)
    
    playlist_id = serializers.UUIDField(source='playlist.playlist_id', read_only=True)
    playlist_name = serializers.CharField(source='playlist.playlist_name', read_only=True)
    playlist_privacy = serializers.CharField(source='playlist.playlist_privacy', read_only=True)
    playlist_banner = serializers.CharField(source='playlist.playlist_banner', read_only=True)
    playlist_likes_counter = serializers.IntegerField(source='playlist.playlist_likes_counter', read_only=True)
    playlist_tracks_counter = serializers.IntegerField(source='playlist.playlist_tracks_counter', read_only=True)

    playlist_position_string = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = PlaylistsByProfile

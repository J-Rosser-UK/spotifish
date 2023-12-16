from rest_framework import serializers
from base.models import Tracks, Profiles, Playlists, Albums, TracksByAlbum, TracksByPlaylist
from django.utils import timezone

class TracksSerializer(serializers.Serializer):

    profile_id = serializers.UUIDField(source='profile.profile_id', read_only=True)
    profile_type = serializers.CharField(source='profile.profile_type', read_only=True)
    profile_privacy = serializers.CharField(source='profile.profile_privacy', read_only=True)
    profile_name = serializers.CharField(source='profile.profile_name', read_only=True)
    profile_handle = serializers.CharField(source='profile.profile_handle', read_only=True)
    profile_picture = serializers.CharField(source='profile.profile_picture', read_only=True)
    

    track_id = serializers.UUIDField()
    track_original_id = serializers.CharField(required=False, allow_null=True)
    track_name = serializers.CharField()
    track_lyrics = serializers.CharField(required=False, allow_null=True)
    track_popularity = serializers.IntegerField(required=False, allow_null=True)
    album = serializers.PrimaryKeyRelatedField(queryset=Albums.objects.all())
    track_danceability = serializers.FloatField(required=False, allow_null=True)
    track_energy = serializers.FloatField(required=False, allow_null=True)
    track_key = serializers.IntegerField(required=False, allow_null=True)
    track_loudness = serializers.FloatField(required=False, allow_null=True)
    track_mode = serializers.IntegerField(required=False, allow_null=True)
    track_speechiness = serializers.FloatField(required=False, allow_null=True)
    track_acousticness = serializers.FloatField(required=False, allow_null=True)
    track_instrumentalness = serializers.FloatField(required=False, allow_null=True)
    track_liveness = serializers.FloatField(required=False, allow_null=True)
    track_valence = serializers.FloatField(required=False, allow_null=True)
    track_tempo = serializers.FloatField(required=False, allow_null=True)
    track_duration_ms = serializers.IntegerField(required=False, allow_null=True)
    track_language = serializers.CharField(required=False, allow_null=True)
    track_soundcloud_link = serializers.CharField(required=False, allow_null=True)
    track_upload_timestamp = serializers.DateTimeField(required=False, allow_null=True, default=timezone.now)
    track_upload_source = serializers.CharField(required=False, allow_null=True)
    track_likes_counter = serializers.IntegerField(default=0)
    track_comments_counter = serializers.IntegerField(default=0)

    class Meta:
        model = Tracks
    

class TracksByAlbumSerializer(serializers.Serializer):

    album_id = serializers.UUIDField(source='album.album_id', read_only=True)
    album_name = serializers.CharField(source='album.album_name', read_only=True)
    album_banner = serializers.CharField(source='album.album_banner', read_only=True)
    album_release_date = serializers.DateTimeField(source='album.album_release_date', read_only=True)
    album_likes_counter = serializers.IntegerField(source='album.album_likes_counter', read_only=True)
    album_tracks_counter = serializers.IntegerField(source='album.album_tracks_counter', read_only=True)


    track = serializers.PrimaryKeyRelatedField(queryset=Tracks.objects.all())
    track_id = serializers.UUIDField(source='track.track_id', read_only=True)
    track_name = serializers.CharField(source='track.track_name', read_only=True)

    profile_id = serializers.UUIDField(source='track.profile.profile_id', read_only=True)
    profile_type = serializers.CharField(source='track.profile.profile_type', read_only=True)
    profile_privacy = serializers.CharField(source='track.profile.profile_privacy', read_only=True)
    profile_name = serializers.CharField(source='track.profile.profile_name', read_only=True)
    profile_handle = serializers.CharField(source='track.profile.profile_handle', read_only=True)
    profile_picture = serializers.CharField(source='track.profile.profile_picture', read_only=True)

    track_position_string = serializers.CharField()

    class Meta:
        model = TracksByAlbum



class TracksByPlaylistSerializer(serializers.Serializer):

    playlist_id = serializers.UUIDField(source='playlist.playlist_id', read_only=True)
    playlist_name = serializers.CharField(source='playlist.playlist_name', read_only=True)
    playlist_privacy = serializers.CharField(source='playlist.playlist_privacy', read_only=True)
    playlist_type = serializers.CharField(source='playlist.playlist_type', read_only=True)
    playlist_banner = serializers.CharField(source='playlist.playlist_banner', read_only=True)
    playlist_likes_counter = serializers.IntegerField(source='playlist.playlist_likes_counter', read_only=True)
    playlist_tracks_counter = serializers.IntegerField(source='playlist.playlist_tracks_counter', read_only=True)

    track = serializers.PrimaryKeyRelatedField(queryset=Tracks.objects.all())
    track_id = serializers.UUIDField(source='track.track_id', read_only=True)
    track_name = serializers.CharField(source='track.track_name', read_only=True)

    profile_id = serializers.UUIDField(source='track.profile.profile_id', read_only=True)
    profile_type = serializers.CharField(source='track.profile.profile_type', read_only=True)
    profile_privacy = serializers.CharField(source='track.profile.profile_privacy', read_only=True)
    profile_name = serializers.CharField(source='track.profile.profile_name', read_only=True)
    profile_handle = serializers.CharField(source='track.profile.profile_handle', read_only=True)
    profile_picture = serializers.CharField(source='track.profile.profile_picture', read_only=True)


    track_position_string = serializers.CharField()

    class Meta:
        model = TracksByPlaylist


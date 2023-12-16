from django.db import models
from cpkmodel import CPkModel
from custom_fields import CustomJSONField
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

class Playlists(models.Model):
    playlist_id = models.UUIDField(primary_key=True)
    playlist_original_id = models.TextField(blank=True, null=True)
    playlist_name = models.TextField()
    playlist_genre = models.TextField(blank=True, null=True)
    playlist_subgenre = models.TextField(blank=True, null=True)
    playlist_privacy = models.TextField()
    playlist_banner = models.TextField(blank=True, null=True)
    playlist_description = models.TextField(blank=True, null=True)
    playlist_links = CustomJSONField(blank=True, null=True)   
    playlist_upload_timestamp = models.DateTimeField(blank=True, null=True, default=timezone.now)
    playlist_upload_source = models.TextField(blank=True, null=True)
    playlist_likes_counter = models.IntegerField(default=0)
    playlist_tracks_counter = models.IntegerField(default=0)
    playlist_admin_list = ArrayField(models.UUIDField(blank=True), blank=True, default=list)

    class Meta:
        managed = False
        db_table = 'playlists'



class PlaylistsByProfile(CPkModel):
    profile = models.ForeignKey('Profiles', on_delete=models.CASCADE, primary_key=True, related_name="playlists_by_profile_profile")
    playlist = models.ForeignKey('Playlists', on_delete=models.CASCADE, primary_key=True, related_name="playlists_by_profile_playlist")
    playlist_position_string = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'playlists_by_profile'
        unique_together = (('profile', 'playlist'),)
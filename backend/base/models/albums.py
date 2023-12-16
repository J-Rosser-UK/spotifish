from django.db import models
from custom_fields import CustomJSONField
from django.utils import timezone

class Albums(models.Model):
    album_id = models.UUIDField(primary_key=True)
    album_original_id = models.TextField(blank=True, null=True)
    album_name = models.TextField()
    album_banner = models.TextField(blank=True, null=True)
    album_release_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    album_links = CustomJSONField(blank=True, null=True)    
    album_upload_timestamp = models.DateTimeField(blank=True, null=True, default=timezone.now)
    album_upload_source = models.TextField(blank=True, null=True)
    album_likes_counter = models.IntegerField(default=0)
    album_tracks_counter = models.IntegerField(default=0)
    profile = models.ForeignKey('Profiles', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'albums'
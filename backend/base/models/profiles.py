
from django.db import models
from custom_fields import CustomJSONField
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

class Profiles(models.Model):
    profile_id = models.UUIDField(primary_key=True)
    profile_type = models.TextField()
    profile_privacy = models.TextField()
    profile_name = models.TextField(blank=True, null=True)
    profile_handle = models.TextField(unique=True)
    profile_picture = models.TextField(blank=True, null=True)
    profile_links = CustomJSONField(blank=True, null=True)   
    profile_upload_timestamp = models.DateTimeField(blank=True, null=True, default=timezone.now)
    profile_upload_source = models.TextField(blank=True, null=True)
    profile_followers_counter = models.IntegerField(default=0)
    profile_following_counter = models.IntegerField(default=0)
    profile_requests_counter = models.IntegerField(blank=True, null=True)
    profile_superuser_list = ArrayField(models.UUIDField(blank=True), blank=True, default=list)
    profile_verification = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profiles'
from django.db import models
from cpkmodel import CPkModel
from django.utils import timezone

class FollowersByProfile(CPkModel):
    profile = models.ForeignKey('Profiles', on_delete=models.CASCADE, primary_key=True, related_name="followers_by_profile_profile")
    follower_profile = models.ForeignKey('Profiles', on_delete=models.CASCADE, primary_key=True, related_name="followers_by_profile_follower_profile")
    follower_type = models.TextField()
    follower_timestamp = models.DateTimeField(blank=True, null=True, default=timezone.now)

    class Meta:
        managed = False
        db_table = 'followers_by_profile'
        unique_together = (('profile', 'follower_profile'),)


class FollowingByProfile(CPkModel):
    profile = models.ForeignKey('Profiles', on_delete=models.CASCADE, primary_key=True, related_name="following_by_profile_profile")
    following_profile = models.ForeignKey('Profiles', on_delete=models.CASCADE, primary_key=True, related_name="following_by_profile_following_profile")
    following_timestamp = models.DateTimeField(blank=True, null=True, default=timezone.now)

    class Meta:
        managed = False
        db_table = 'following_by_profile'
        unique_together = (('profile', 'following_profile'),)


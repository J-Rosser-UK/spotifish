
from django.db import models
from .profiles import Profiles
from .albums import Albums
from .playlists import Playlists
from cpkmodel import CPkModel
from django.utils import timezone

class Tracks(models.Model):
    track_id = models.UUIDField(primary_key=True)
    track_original_id = models.TextField(blank=True, null=True)
    track_name = models.TextField()
    profile = models.ForeignKey(Profiles, on_delete=models.CASCADE)
    track_lyrics = models.TextField(blank=True, null=True)
    track_popularity = models.IntegerField(blank=True, null=True)
    album = models.ForeignKey(Albums, on_delete=models.CASCADE)
    track_danceability = models.FloatField(blank=True, null=True)
    track_energy = models.FloatField(blank=True, null=True)
    track_key = models.IntegerField(blank=True, null=True)
    track_loudness = models.FloatField(blank=True, null=True)
    track_mode = models.IntegerField(blank=True, null=True)
    track_speechiness = models.FloatField(blank=True, null=True)
    track_acousticness = models.FloatField(blank=True, null=True)
    track_instrumentalness = models.FloatField(blank=True, null=True)
    track_liveness = models.FloatField(blank=True, null=True)
    track_valence = models.FloatField(blank=True, null=True)
    track_tempo = models.FloatField(blank=True, null=True)
    track_duration_ms = models.IntegerField(blank=True, null=True)
    track_language = models.TextField(blank=True, null=True)
    track_soundcloud_link = models.TextField(blank=True, null=True)
    track_upload_timestamp = models.DateTimeField(blank=True, null=True, default=timezone.now)
    track_upload_source = models.TextField(blank=True, null=True)
    track_likes_counter = models.IntegerField(default=0)
    track_comments_counter = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'tracks'


class TracksByAlbum(CPkModel):
    album = models.ForeignKey('Albums', on_delete=models.CASCADE, primary_key=True, related_name="tracks_by_album_album")
    track = models.ForeignKey('Tracks', on_delete=models.CASCADE, primary_key=True, related_name="tracks_by_album_track")
    track_position_string = models.TextField()

    class Meta:
        managed = False
        db_table = 'tracks_by_album'
        unique_together = (('album', 'track'),)


class TracksByPlaylist(CPkModel):
    playlist = models.ForeignKey('Playlists', on_delete=models.CASCADE, primary_key=True, related_name="tracks_by_playlist_playlist")
    track = models.ForeignKey('Tracks', on_delete=models.CASCADE, primary_key=True, related_name = "tracks_by_playlist_tracks")
    track_position_string = models.TextField()

    class Meta:
        managed = False
        db_table = 'tracks_by_playlist'
        unique_together = (('playlist', 'track'),)

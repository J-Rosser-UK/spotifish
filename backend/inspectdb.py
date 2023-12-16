# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountEmailaddress(models.Model):
    email = models.CharField(unique=True, max_length=254)
    verified = models.BooleanField()
    primary = models.BooleanField()
    user = models.ForeignKey('AdministrationAccount', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailaddress'


class AccountEmailconfirmation(models.Model):
    created = models.DateTimeField()
    sent = models.DateTimeField(blank=True, null=True, default=timezone.now)
    key = models.CharField(unique=True, max_length=64)
    email_address = models.ForeignKey(AccountEmailaddress, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailconfirmation'


class AdministrationAccount(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True, default=timezone.now)
    profile_id = models.UUIDField(unique=True)
    email = models.CharField(unique=True, max_length=254)
    username = models.CharField(unique=True, max_length=30)
    fullname = models.CharField(max_length=150)
    date_joined = models.DateTimeField(blank=True, null=True, default=timezone.now)
    is_staff = models.BooleanField()
    is_superuser = models.BooleanField()
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'administration_account'


class AdministrationAccountGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(AdministrationAccount, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'administration_account_groups'
        unique_together = (('account', 'group'),)


class AdministrationAccountUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(AdministrationAccount, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'administration_account_user_permissions'
        unique_together = (('account', 'permission'),)


class Albums(models.Model):
    album_id = models.UUIDField(primary_key=True)
    album_original_id = models.TextField(blank=True, null=True)
    album_name = models.TextField()
    album_banner = models.TextField(blank=True, null=True)
    album_release_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    album_links = models.TextField(blank=True, null=True)  # This field type is a guess.
    album_upload_timestamp = models.DateTimeField(blank=True, null=True, default=timezone.now)
    album_upload_source = models.TextField(blank=True, null=True)
    album_likes_counter = models.IntegerField()
    album_tracks_counter = models.IntegerField()
    profile = models.ForeignKey('Profiles', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'albums'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AdministrationAccount, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AdministrationAccount, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class FollowersByProfile(models.Model):
    profile = models.OneToOneField('Profiles', models.DO_NOTHING, primary_key=True)
    follower_profile = models.ForeignKey('Profiles', models.DO_NOTHING)
    follower_type = models.TextField()
    follower_timestamp = models.DateTimeField(blank=True, null=True, default=timezone.now)

    class Meta:
        managed = False
        db_table = 'followers_by_profile'
        unique_together = (('profile', 'follower_profile'),)


class FollowingByProfile(models.Model):
    profile = models.OneToOneField('Profiles', models.DO_NOTHING, primary_key=True)
    following_profile = models.ForeignKey('Profiles', models.DO_NOTHING)
    following_timestamp = models.DateTimeField(blank=True, null=True, default=timezone.now)

    class Meta:
        managed = False
        db_table = 'following_by_profile'
        unique_together = (('profile', 'following_profile'),)


class Oauth2ProviderAccesstoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.CharField(unique=True, max_length=255)
    expires = models.DateTimeField()
    scope = models.TextField()
    application = models.ForeignKey('Oauth2ProviderApplication', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AdministrationAccount, models.DO_NOTHING, blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    source_refresh_token = models.OneToOneField('Oauth2ProviderRefreshtoken', models.DO_NOTHING, blank=True, null=True)
    id_token = models.OneToOneField('Oauth2ProviderIdtoken', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_accesstoken'


class Oauth2ProviderApplication(models.Model):
    id = models.BigAutoField(primary_key=True)
    client_id = models.CharField(unique=True, max_length=100)
    redirect_uris = models.TextField()
    client_type = models.CharField(max_length=32)
    authorization_grant_type = models.CharField(max_length=32)
    client_secret = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(AdministrationAccount, models.DO_NOTHING, blank=True, null=True)
    skip_authorization = models.BooleanField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    algorithm = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_application'


class Oauth2ProviderGrant(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=255)
    expires = models.DateTimeField()
    redirect_uri = models.TextField()
    scope = models.TextField()
    application = models.ForeignKey(Oauth2ProviderApplication, models.DO_NOTHING)
    user = models.ForeignKey(AdministrationAccount, models.DO_NOTHING)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    code_challenge = models.CharField(max_length=128)
    code_challenge_method = models.CharField(max_length=10)
    nonce = models.CharField(max_length=255)
    claims = models.TextField()

    class Meta:
        managed = False
        db_table = 'oauth2_provider_grant'


class Oauth2ProviderIdtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    jti = models.UUIDField(unique=True)
    expires = models.DateTimeField()
    scope = models.TextField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    application = models.ForeignKey(Oauth2ProviderApplication, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AdministrationAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_idtoken'


class Oauth2ProviderRefreshtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.CharField(max_length=255)
    access_token = models.OneToOneField(Oauth2ProviderAccesstoken, models.DO_NOTHING, blank=True, null=True)
    application = models.ForeignKey(Oauth2ProviderApplication, models.DO_NOTHING)
    user = models.ForeignKey(AdministrationAccount, models.DO_NOTHING)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    revoked = models.DateTimeField(blank=True, null=True, default=timezone.now)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_refreshtoken'
        unique_together = (('token', 'revoked'),)


class Playlists(models.Model):
    playlist_id = models.UUIDField(primary_key=True)
    playlist_original_id = models.TextField(blank=True, null=True)
    playlist_name = models.TextField()
    playlist_genre = models.TextField(blank=True, null=True)
    playlist_subgenre = models.TextField(blank=True, null=True)
    playlist_privacy = models.TextField()
    playlist_banner = models.TextField(blank=True, null=True)
    playlist_description = models.TextField(blank=True, null=True)
    playlist_links = models.TextField(blank=True, null=True)  # This field type is a guess.
    playlist_upload_timestamp = models.DateTimeField(blank=True, null=True, default=timezone.now)
    playlist_upload_source = models.TextField(blank=True, null=True)
    playlist_likes_counter = models.IntegerField()
    playlist_tracks_counter = models.IntegerField()
    playlist_admin_list = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'playlists'


class PlaylistsByProfile(models.Model):
    profile = models.OneToOneField('Profiles', models.DO_NOTHING, primary_key=True)
    playlist = models.ForeignKey(Playlists, models.DO_NOTHING)
    playlist_position_string = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'playlists_by_profile'
        unique_together = (('profile', 'playlist'),)


class Profiles(models.Model):
    profile_id = models.UUIDField(primary_key=True)
    profile_type = models.TextField()
    profile_privacy = models.TextField()
    profile_name = models.TextField(blank=True, null=True)
    profile_handle = models.TextField(unique=True)
    profile_picture = models.TextField(blank=True, null=True)
    profile_links = models.TextField(blank=True, null=True)  # This field type is a guess.
    profile_upload_timestamp = models.DateTimeField(blank=True, null=True, default=timezone.now)
    profile_upload_source = models.TextField(blank=True, null=True)
    profile_followers_counter = models.IntegerField()
    profile_following_counter = models.IntegerField()
    profile_requests_counter = models.IntegerField(blank=True, null=True)
    profile_superuser_list = models.TextField(blank=True, null=True)  # This field type is a guess.
    profile_verification = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profiles'


class SocialaccountSocialaccount(models.Model):
    provider = models.CharField(max_length=30)
    uid = models.CharField(max_length=191)
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    extra_data = models.TextField()
    user = models.ForeignKey(AdministrationAccount, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialaccount'
        unique_together = (('provider', 'uid'),)


class SocialaccountSocialapp(models.Model):
    provider = models.CharField(max_length=30)
    name = models.CharField(max_length=40)
    client_id = models.CharField(max_length=191)
    secret = models.CharField(max_length=191)
    key = models.CharField(max_length=191)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp'


class SocialaccountSocialappSites(models.Model):
    id = models.BigAutoField(primary_key=True)
    socialapp = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING)
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp_sites'
        unique_together = (('socialapp', 'site'),)


class SocialaccountSocialtoken(models.Model):
    token = models.TextField()
    token_secret = models.TextField()
    expires_at = models.DateTimeField(blank=True, null=True, default=timezone.now)
    account = models.ForeignKey(SocialaccountSocialaccount, models.DO_NOTHING)
    app = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialtoken'
        unique_together = (('app', 'account'),)


class TokenBlacklistBlacklistedtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    blacklisted_at = models.DateTimeField()
    token = models.OneToOneField('TokenBlacklistOutstandingtoken', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'token_blacklist_blacklistedtoken'


class TokenBlacklistOutstandingtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True, default=timezone.now)
    expires_at = models.DateTimeField()
    user = models.ForeignKey(AdministrationAccount, models.DO_NOTHING, blank=True, null=True)
    jti = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'token_blacklist_outstandingtoken'


class Tracks(models.Model):
    track_id = models.UUIDField(primary_key=True)
    track_original_id = models.TextField(blank=True, null=True)
    track_name = models.TextField()
    profile = models.ForeignKey(Profiles, models.DO_NOTHING)
    track_lyrics = models.TextField(blank=True, null=True)
    track_popularity = models.IntegerField(blank=True, null=True)
    album = models.ForeignKey(Albums, models.DO_NOTHING)
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
    track_likes_counter = models.IntegerField()
    track_comments_counter = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tracks'


class TracksByAlbum(models.Model):
    album = models.OneToOneField(Albums, models.DO_NOTHING, primary_key=True)
    track = models.ForeignKey(Tracks, models.DO_NOTHING)
    track_position_string = models.TextField()

    class Meta:
        managed = False
        db_table = 'tracks_by_album'
        unique_together = (('album', 'track'),)


class TracksByPlaylist(models.Model):
    playlist = models.OneToOneField(Playlists, models.DO_NOTHING, primary_key=True)
    track = models.ForeignKey(Tracks, models.DO_NOTHING)
    track_position_string = models.TextField()

    class Meta:
        managed = False
        db_table = 'tracks_by_playlist'
        unique_together = (('playlist', 'track'),)

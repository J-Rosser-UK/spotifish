

import uuid
from base.models import Profiles, Playlists, PlaylistsByProfile

class SignUpFactory:
   
    def __init__(self, request, data):
        
        self.request = request
        self.data = data
        self.profile_id = data.get("profile_id") if data.get("profile_id") else str(uuid.uuid4())
        self.request.user.profile_id = self.profile_id
        self.favourites_playlist_id  = str(uuid.uuid4())

    def create(self):

        profile = self.create_profile()
        playlist, playlist_by_profile = self.create_favourites_playlist(profile)
        return profile

    def create_profile(self):
        
        profile = Profiles.objects.create(
            profile_id = self.data.get("profile_id"),
            profile_type = self.data.get("profile_type") if isinstance(self.data.get("profile_type"), str) else "user",
            profile_privacy = self.data.get("profile_privacy") if isinstance(self.data.get("profile_privacy"), str) else "public",
            profile_name = self.data.get("profile_name") if isinstance(self.data.get("profile_name"), str) else None,
            profile_handle = self.data.get("username"),
            profile_superuser_list = [self.data.get("profile_id")],
            profile_verification = self.data.get("profile_verification") if isinstance(self.data.get("profile_verification"), str) else None
            )
        
        return profile

    def create_favourites_playlist(self, profile):

        playlist = Playlists.objects.create(
            playlist_id = self.favourites_playlist_id,
            playlist_privacy='private',
            playlist_type='favourites',
            playlist_name='Favourites',
            profile_id=profile.profile_id
        )

        playlist_by_profile = PlaylistsByProfile.objects.create(
            profile_id=profile.profile_id,
            playlist_id = self.favourites_playlist_id,
            playlist_position_string="aaa"
        )

        return playlist, playlist_by_profile


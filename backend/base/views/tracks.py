from rest_framework.viewsets import ViewSet
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.urls import path, include
from django.db.models import Q

from base.models import Tracks, TracksByPlaylist
from base.serializers import TracksSerializer, TracksByPlaylistSerializer
from base.utilz.lexorank import LexoRank

import uuid

from backend.settings import PAGINATION_SIZE

class TracksViewSet(ViewSet):

    model = Tracks
    serializer = TracksSerializer

    def __init__(self):

        self.not_null = [
            "track_id",
            "track_type",
            "track_privacy",
            "track_handle",
            "track_upload_timestamp",
          
        ]

        self.frozen = [
            "track_id",
            "track_upload_timestamp",
        
        ]

    def create(self, request):
        
        profile_id_pk = request.user.profile_id
        track_id_pk = request.data.get("track_id") if request.data.get("track_id") else str(uuid.uuid4())
        playlist_id_pk = request.data.get("playlist_id") if request.data.get("playlist_id") else str(uuid.uuid4())

        # Create track object
        obj = Tracks.objects.create(
            playlist_id = playlist_id_pk,
            track_id = track_id_pk,
            track_name = request.data.get("track_name"),
            track_banner = request.data.get("track_banner"),
            track_description = request.data.get("track_description"),
            track_links = request.data.get("track_links"),
            track_privacy = request.data.get("track_privacy", "private"),
            track_admin_list = request.data.get("track_admin_list"),
            track_type = request.data.get("track_type", "by_user")
        )

        # Attempt to retrieve the first track by profile that is not of type "favourites"
        first_track_by_playlist = TracksByPlaylist.objects.filter(
            playlist_id = playlist_id_pk
        ).order_by('track_position_string').first()

        # Check if a track was found, if not use the reserved end rank
        if first_track_by_playlist is not None:
            first_track_position_string = first_track_by_playlist.track_position_string
        else:
            first_track_position_string = LexoRank.RESERVED_END
        
        track_position_string_pk = LexoRank.calculate_top(first_track_position_string)

        # Create tracks by profile object
        obj = TracksByPlaylist.objects.create(
            track_id = track_id_pk,
            playlist_id = playlist_id_pk,
            track_position_string = track_position_string_pk
        )

        obj.save()

        response = TracksByPlaylistSerializer(obj, context={'request': request}).data
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, track_id_pk):
        """ Retrieve single profile. """

        obj = get_object_or_404(Tracks, track_id = track_id_pk)

        response = TracksSerializer(obj, context={"request": request}).data

        return Response(response, status=status.HTTP_200_OK)
    
    def list_paginated(self, request, profile_id_pk, cursor):
        """Retrieves tracks associated with a profile, applying permissions for filtering."""

        response_data = {"tracks": []}
        
        if cursor == "first_page":

            tracks_query = TracksByPlaylist.objects.filter(
                profile_id=profile_id_pk
            )

            tracks_query = tracks_query.order_by('track_position_string')[:PAGINATION_SIZE]
            response_data["tracks"] = [TracksByPlaylistSerializer(track, context={'request': request}).data 
                    for track in tracks_query if track]

        else:
            tracks_query = TracksByPlaylist.objects.filter(
                Q(profile_id=profile_id_pk) & Q(track_position_string__gt=cursor)
            )

            tracks_query = tracks_query.order_by('track_position_string')[:PAGINATION_SIZE]
            response_data["tracks"] = [TracksByPlaylistSerializer(track, context={'request': request}).data 
                    for track in tracks_query if track]

        if not any(response_data.values()):
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        
        return Response(response_data, status=status.HTTP_200_OK)


    
    def update(self, request):

        pass

    def destroy(self, request, track_id_pk):
        """ Destroys profile and cascades to destroy objects """

        
        # get profile object
        obj = get_object_or_404(Tracks, track_id = track_id_pk)

        if str(obj.profile_id) == str(request.user.profile_id):

            # delete the profile (cascades)
            obj.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        else:

            return Response(status=status.HTTP_403_FORBIDDEN)
      

    

urlpatterns = [

    path('api/tracks/create', TracksViewSet.as_view({'post': 'create'}), name = 'tracks_viewset_create'),
    path('api/tracks/<str:track_id_pk>/retrieve', TracksViewSet.as_view({'get': 'retrieve'}), name = 'tracks_viewset_retrieve'),
    path('api/tracks/<str:profile_id_pk>/<str:cursor>/list_paginated', TracksViewSet.as_view({'get': 'list_paginated'}), name = 'tracks_viewset_list_paginated'),
    # path('api/tracks/<str:track_id_pk>/update', TracksViewSet.as_view({'patch': 'update'}), name = 'tracks_viewset_update'),
    path('api/tracks/<str:track_id_pk>/destroy', TracksViewSet.as_view({'delete': 'destroy'}), name = 'tracks_viewset_destroy'),

]


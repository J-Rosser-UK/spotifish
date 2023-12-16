from rest_framework.viewsets import ViewSet
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.urls import path, include
from django.db.models import Q

from base.models import Playlists, PlaylistsByProfile
from base.serializers import PlaylistsSerializer, PlaylistsByProfileSerializer
from base.utilz.lexorank import LexoRank

import uuid

from backend.settings import PAGINATION_SIZE

class PlaylistsViewSet(ViewSet):

    model = Playlists
    serializer = PlaylistsSerializer

    def __init__(self):

        self.not_null = [
            "playlist_id",
            "playlist_type",
            "playlist_privacy",
            "playlist_handle",
            "playlist_upload_timestamp",
          
        ]

        self.frozen = [
            "playlist_id",
            "playlist_upload_timestamp",
        
        ]

    def create(self, request):
        
        profile_id_pk = request.user.profile_id
        playlist_id_pk = request.data.get("playlist_id") if request.data.get("playlist_id") else str(uuid.uuid4())

        # Create playlist object
        obj = Playlists.objects.create(
            profile_id = profile_id_pk,
            playlist_id = playlist_id_pk,
            playlist_name = request.data.get("playlist_name"),
            playlist_banner = request.data.get("playlist_banner"),
            playlist_description = request.data.get("playlist_description"),
            playlist_links = request.data.get("playlist_links"),
            playlist_privacy = request.data.get("playlist_privacy", "private"),
            playlist_admin_list = request.data.get("playlist_admin_list"),
            playlist_type = request.data.get("playlist_type", "by_user")
        )

        # Attempt to retrieve the first playlist by profile that is not of type "favourites"
        first_playlist_by_profile = PlaylistsByProfile.objects.filter(
            profile_id = profile_id_pk
        ).exclude(
            playlist_type = "favourites"
        ).order_by('playlist_position_string').first()

        # Check if a playlist was found, if not use the reserved end rank
        if first_playlist_by_profile is not None:
            first_playlist_position_string = first_playlist_by_profile.playlist_position_string
        else:
            first_playlist_position_string = LexoRank.RESERVED_END
        
        playlist_position_string_pk = LexoRank.calculate_top(first_playlist_position_string)

        # Create playlists by profile object
        obj = PlaylistsByProfile.objects.create(
            playlist_id = playlist_id_pk,
            profile_id = profile_id_pk,
            playlist_position_string = playlist_position_string_pk
        )

        obj.save()

        response = PlaylistsByProfileSerializer(obj, context={'request': request}).data
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, playlist_id_pk):
        """ Retrieve single profile. """

        obj = get_object_or_404(Playlists, playlist_id = playlist_id_pk)

        response = PlaylistsSerializer(obj, context={"request": request}).data

        return Response(response, status=status.HTTP_200_OK)
    
    def list_paginated(self, request, profile_id_pk, cursor):
        """Retrieves playlists associated with a profile, applying permissions for filtering."""

        is_own_profile = str(profile_id_pk) == str(request.user.profile_id)
        response_data = {"favourites": [], "playlists": []}
        
        # If first page, also look for the favourites playlist
        if cursor == "first_page":
           
            if is_own_profile:
                
                favourites_query = PlaylistsByProfile.objects.filter(
                    Q(profile_id=profile_id_pk) & Q(playlist__playlist_type="favourites")
                )
                response_data["favourites"] = [PlaylistsByProfileSerializer(playlist, context={'request': request}).data 
                    for playlist in favourites_query if playlist]

            playlists_query = PlaylistsByProfile.objects.filter(
                profile_id=profile_id_pk
            ).exclude(Q(playlist__playlist_type="favourites"))

            playlists_query = playlists_query.order_by('playlist_position_string')[:PAGINATION_SIZE]
            response_data["playlists"] = [PlaylistsByProfileSerializer(playlist, context={'request': request}).data 
                    for playlist in playlists_query if playlist]

        else:
            playlists_query = PlaylistsByProfile.objects.filter(
                Q(profile_id=profile_id_pk) & Q(playlist_position_string__gt=cursor)
            ).exclude(Q(playlist__playlist_type="favourites"))

            playlists_query = playlists_query.order_by('playlist_position_string')[:PAGINATION_SIZE]
            response_data["playlists"] = [PlaylistsByProfileSerializer(playlist, context={'request': request}).data 
                    for playlist in playlists_query if playlist]

        if not any(response_data.values()):
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        
        return Response(response_data, status=status.HTTP_200_OK)


    
    def update(self, request):

        pass

    def destroy(self, request, playlist_id_pk):
        """ Destroys profile and cascades to destroy objects """

        
        # get profile object
        obj = get_object_or_404(Playlists, playlist_id = playlist_id_pk)

        if str(obj.profile_id) == str(request.user.profile_id):

            # delete the profile (cascades)
            obj.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        else:

            return Response(status=status.HTTP_403_FORBIDDEN)
      

    

urlpatterns = [

    path('api/playlists/create', PlaylistsViewSet.as_view({'post': 'create'}), name = 'playlists_viewset_create'),
    path('api/playlists/<str:playlist_id_pk>/retrieve', PlaylistsViewSet.as_view({'get': 'retrieve'}), name = 'playlists_viewset_retrieve'),
    path('api/playlists/<str:profile_id_pk>/<str:cursor>/list_paginated', PlaylistsViewSet.as_view({'get': 'list_paginated'}), name = 'playlists_viewset_list_paginated'),
    # path('api/playlists/<str:playlist_id_pk>/update', PlaylistsViewSet.as_view({'patch': 'update'}), name = 'playlists_viewset_update'),
    path('api/playlists/<str:playlist_id_pk>/destroy', PlaylistsViewSet.as_view({'delete': 'destroy'}), name = 'playlists_viewset_destroy'),

]


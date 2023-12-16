from rest_framework.viewsets import ViewSet
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.shortcuts import get_object_or_404, get_list_or_404
from django.urls import path, include

from base.models import Albums
from base.serializers import AlbumsSerializer

class AlbumsViewSet(ViewSet):

    model = Albums
    serializer = AlbumsSerializer

    def __init__(self):

        self.not_null = [
            "album_id",
            "album_type",
            "album_privacy",
            "album_handle",
            "album_upload_timestamp",
          
        ]

        self.frozen = [
            "album_id",
            "album_upload_timestamp",
        
        ]

    def create(self, request):
        
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def retrieve(self, request, profile_id_pk):
        """ Retrieve single profile. """

        obj = get_object_or_404(Albums, profile_id = profile_id_pk)

        response = AlbumsSerializer(obj, context={"request": request}).data

        return Response(response, status=status.HTTP_200_OK)
    
    def list(self, request, profile_id_pk):

        albums_query = get_list_or_404(Albums, profile_id = profile_id_pk)

        response = [AlbumsSerializer(album, context={'request': request}).data 
                    for album in albums_query if album]
        
        return Response(response, status=status.HTTP_200_OK)
    
    def update(self, request):

        pass

    def destroy(self, request, profile_id_pk):
        """ Destroys profile and cascades to destroy objects """

        if profile_id_pk == str(request.user.profile_id):
            # get profile object
            obj = get_object_or_404(Albums, profile_id = profile_id_pk)

            # delete the profile (cascades)
            obj.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
       
        return Response(status=status.HTTP_403_FORBIDDEN)

    

urlpatterns = [

    path('api/albums/create', AlbumsViewSet.as_view({'post': 'create'}), name = 'albums_viewset_create'),
    path('api/albums/<str:profile_id_pk>/retrieve', AlbumsViewSet.as_view({'get': 'retrieve'}), name = 'albums_viewset_retrieve'),
    path('api/albums/<str:profile_id_pk>/list', AlbumsViewSet.as_view({'get': 'list'}), name = 'albums_viewset_list'),
    # path('api/albums/<str:profile_id_pk>/update', AlbumsViewSet.as_view({'patch': 'update'}), name = 'albums_viewset_update'),
    path('api/albums/<str:profile_id_pk>/destroy', AlbumsViewSet.as_view({'delete': 'destroy'}), name = 'albums_viewset_destroy'),

]


from rest_framework.viewsets import ViewSet
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.urls import path, include

from base.models import Profiles
from base.serializers import ProfilesSerializer

class ProfilesViewSet(ViewSet):

    model = Profiles
    serializer = ProfilesSerializer

    def __init__(self):

        self.not_null = [
            "profile_id",
            "profile_type",
            "profile_privacy",
            "profile_handle",
            "profile_upload_timestamp",
            "profile_followers_counter",
            "profile_following_counter"
        ]

        self.frozen = [
            "profile_id",
            "profile_upload_timestamp",
            "profile_followers_counter",
            "profile_following_counter"
        ]

    def create(self, request):
        """ Profiles cannot be created without creating an Account. """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def retrieve(self, request, profile_id_pk):
        """ Retrieve single profile. """

        obj = get_object_or_404(Profiles, profile_id = profile_id_pk)

        response = ProfilesSerializer(obj, context={"request": request}).data

        return Response(response, status=status.HTTP_200_OK)
    
    def list(self, request):

        pass
    
    def update(self, request):

        pass

    def destroy(self, request, profile_id_pk):
        """ Destroys profile and cascades to destroy objects """

        if profile_id_pk == str(request.user.profile_id):
            # get profile object
            obj = get_object_or_404(Profiles, profile_id = profile_id_pk)

            # delete the profile (cascades)
            obj.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
       
        return Response(status=status.HTTP_403_FORBIDDEN)

    

urlpatterns = [

    path('api/profiles/create', ProfilesViewSet.as_view({'post': 'create'}), name = 'profiles_viewset_create'),
    path('api/profiles/<str:profile_id_pk>/retrieve', ProfilesViewSet.as_view({'get': 'retrieve'}), name = 'profiles_viewset_retrieve'),
    # path('api/profiles/<str:profile_id_pk>/list', ProfilesViewSet.as_view({'get': 'list'}), name = 'profiles_viewset_list'),
    # path('api/profiles/<str:profile_id_pk>/update', ProfilesViewSet.as_view({'patch': 'update'}), name = 'profiles_viewset_update'),
    path('api/profiles/<str:profile_id_pk>/destroy', ProfilesViewSet.as_view({'delete': 'destroy'}), name = 'profiles_viewset_destroy'),

]


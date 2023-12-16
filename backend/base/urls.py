from django.urls import path, include

urlpatterns = [

    path('', include('base.views.albums')),
    # path('', include('base.views.followers')),
    path('', include('base.views.playlists')),
    path('', include('base.views.profiles')),
    # path('', include('base.views.tracks')),

]
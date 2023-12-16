
from django.urls import path, include
from django.contrib import admin
from .views import *
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/signup/', SignUpView.as_view(), name="signup"),       
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),             
    path('api/auth/is_email_available', IsEmailAvailableViewSet.as_view({'post': 'is_email_available'}), name = 'is_email_available'),    
       

    path('api/auth/', include('dj_rest_auth.urls')),                                            
    
]

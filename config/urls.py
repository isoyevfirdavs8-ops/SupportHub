
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from control.views import RegisterView, ProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('control.urls')),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/login/',TokenObtainPairView.as_view(),name='auth_login'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('auth/profile/', ProfileView.as_view(), name='auth_profile'),
]

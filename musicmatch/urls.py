"""musicmatch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from musicapp.views import *
from django.conf.urls.static import static
from django.conf import settings

# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('signup', CreateUserViewSet)
router.register('upload_images', CreateUserImageViewSet)
router.register('profiles', ProfileViewSet)
router.register('genres', GenreViewSet)
router.register('instruments', InstrumentViewSet)
router.register('user_instruments', UserInstrumentViewSet)
router.register('user_genres', UserGenreViewSet)
router.register('user_images', UserImageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('auth/', CustomObtainAuthToken.as_view(), name='login'),
    path('check_user/', CheckUserExists.as_view(), name='check_user'),
    path('set_recommendations/', SetUserRecommendationsView.as_view(), name='set_recommendations'),
    path('get_recommendations/', GetUserRecommendationsView.as_view(), name='get_recommendations'),
    path('update_user/', UpdateUserView.as_view(), name='update_user'),
    path('', include('pwa.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

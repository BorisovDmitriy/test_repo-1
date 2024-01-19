"""
URL configuration for testrepo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from testrepo import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from women.views import pageNotFound, WomenAPIList,WomenAPIUpdate, WomenAPIDestroy#WomenViewSet
from rest_framework import routers

# TODO video 10
# router = routers.DefaultRouter()
# router.register(r'women', WomenViewSet)
# print(router.urls) # для отладки


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/drf-auth/', include('rest_framework.urls')), # Video 11
    path('captcha/', include('captcha.urls')),
    path('', include('women.urls')),  # http://127.0.0.1:8000/women/
    # Добавил видео 10
    path('api/v1/women/', WomenAPIList.as_view()),
    path('api/v1/women/<int:pk>/', WomenAPIUpdate.as_view()),
    path('api/v1/womendelete/<int:pk>/', WomenAPIDestroy.as_view()),
    # Видео 12 Djosver
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    # Убрал видео 10
    #path('api/v1/', include(router.urls)),  # http://127.0.0.1:8000/api/v1/women/

    # path('api/v1/womenlist/', WomenViewSet.as_view({'get': 'list'})),
    # path('api/v1/womenlist/<int:pk>/', WomenViewSet.as_view({'put': 'update'})),
    ]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound

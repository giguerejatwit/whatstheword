"""wtw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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



from Post.views import LikeView
from knox.views import LogoutAllView, LogoutView
from django import urls
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from django.conf import settings
from django.conf.urls.static import static

from Post.views import ArticleViewSet
from accounts.views import ProfilePostsAPI, ProfileAPI, followUser, RegisterAPI, LoginAPI, ChangePasswordView

router = DefaultRouter()
router.register("articles", ArticleViewSet, basename="articles")
router.register("profiles", ProfileAPI, basename="profiles")
router.register("profiles/uploads", ProfilePostsAPI, basename="profile/uploads")
# router.register('wtw/accounts', RegisterAPI, basename='register')
urlpatterns = [
    path("wtw/", include(router.urls)),
    path("admin/", admin.site.urls),
    path("wtw/follow/<int:pk>/", followUser, name="follow"),
    path("wtw/like/<int:pk>/", LikeView, name = 'Like'),
    path("wtw/register/", RegisterAPI.as_view(), name="register"),
    path("wtw/login/", LoginAPI.as_view(), name="login"),
    path("wtw/logout/", LogoutView.as_view(), name="Logout"),
    path("wtw/change-password/", ChangePasswordView.as_view(), name="change_password"),
    # path('wtw/profile/', ProfileAPI.as_view(), name = 'profile')
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

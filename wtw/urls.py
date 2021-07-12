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

from knox.views import LogoutAllView, LogoutView
from accounts.views import RegisterAPI, LoginAPI, ChangePasswordView

from django import urls
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from Post.views import ArticleViewSet

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('wtw/articles', ArticleViewSet, basename = 'articles')
#router.register('wtw/accounts', RegisterAPI, basename='register')
urlpatterns = [
    path('', include(router.urls)),

    path('admin/', admin.site.urls),

    path('wtw/register', RegisterAPI.as_view(), name='register'),
    path('wtw/login/', LoginAPI.as_view(), name = 'login'),
    path('wtw/logout/', LogoutView.as_view(), name ='Logout'),
    path('wtw/change-password', ChangePasswordView.as_view(), name = 'change_password'),

]

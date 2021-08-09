# from Post.decorators import unauthenticated_user
from copy import error

from django.contrib.auth import login
from django.core.checks.messages import ERROR
from django.db.models import query
from django.db.models.query import QuerySet
from django.http import Http404, HttpResponse, JsonResponse
from django.http.response import HttpResponseGone
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic.base import View

# allows us to authenticate tokens from knox auth
from knox.auth import TokenAuthentication
from knox.models import User  # ****
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from Post.models import Article
from Post.serializers import ArticleSerializer
from Post.views import ArticleViewSet
from rest_framework import (
    generics,
    mixins,
    permissions,
    response,
    serializers,
    status,
    views,
    viewsets,
)
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import APIView, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.response import Response
from rest_framework.serializers import Serializer

# from .decorators import promoter_only
from .models import Article, User, UserProfile
from .serializer import (
    ChangePasswordSerializer,
    RegisterSerializer,
    UserProfileSerializer,
    UserSerializer,
)

# from .serializers import ArticleSerializer
class addFollower(View):
    
    def post(self, request, pk, *args, **kwargs):
        #lets get the follower
        profile = UserProfile.objects.get(pk=pk)
        #the current user will be added to the following of the profile being followed
        profile.followers.add(request.user)

class addFollower(View):
    
    def post(self, request, pk, *args, **kwargs):
        #lets get the follower
        profile = UserProfile.objects.get(pk=pk)
        #the current user will be added to the following of the profile being followed
        profile.followers.remove(request.user)


class ProfileAPI(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        try:
            QuerySet = UserProfile.objects.all()
            user = get_object_or_404(QuerySet, pk=pk)
            userSerializers = UserProfileSerializer(user)
            user_id = getattr(user, "user")
            return Response(userSerializers.data)
        except error:
            print(error)


class ProfilePostsAPI(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        try:
            QuerySet = UserProfile.objects.all()
            user = get_object_or_404(QuerySet, pk=pk)
            userSerializers = UserProfileSerializer(user)
            user_id = getattr(user, "user")
            userArticles = Article.objects.filter(author_id=user_id)
            articleSerializer = ArticleSerializer(userArticles, many=True)
            return Response(articleSerializer.data)
        except error:
            print(error)


# Register API
#
###
class RegisterAPI(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                # returns the given fields of UserSerializer
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


#
# LoginAPI
#
# #
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)

        return super(LoginAPI, self).post(request, format=None)


#
# ChangePasswordView
#
# #
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

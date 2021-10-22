# from Post.decorators import unauthenticated_user
from copy import error

from django import db, http
from django.contrib.auth import login
from django.core.checks.messages import ERROR
from django.db.models import query
from django.db.models.query import QuerySet
from django.dispatch.dispatcher import NONE_ID
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
    relations,
    response,
    serializers,
    status,
    views,
    viewsets,
)
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import (
    APIView,
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.fields import to_choices_dict
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.response import Response
from rest_framework.serializers import Serializer

# from .decorators import promoter_only
from .models import FollowerRelation, User, UserProfile
from .serializers import (
    ChangePasswordSerializer,
    ProfileEditSerializer,
    RegisterSerializer,
    UserProfileSerializer,
    UserSerializer,
    ViewUserProfileSerializer,
    followSerializer,
)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def followUser(request, *args, **kwargs):
    # a class to follow a another user
    is_following = False
    prof = request.data.get("profile")

    profile_ = UserProfile.objects.get(user_id=prof)
    profile_username = profile_.user

    user_ = User.objects.get(username=request.user)

    # check follower count of focused profile
    follower_count = profile_.followers.count()
    # check if user is in the list of followers of the profile.followers
    follower_list = profile_.followers.all()

    if user_ in follower_list:
        is_following = True

    if is_following == False:
        relation = FollowerRelation.objects.create(user=user_, profile=profile_)
        profile_.followers.add(user_)

        return Response(
            {
                "isFollowing": True,
                "followCount": follower_count,
                "response": f"{user_.username} followed {profile_username}",
            }
        )

    elif is_following == True:
        relation = FollowerRelation.objects.filter(
            user=user_, profile=profile_
        ).delete()
        profile_.followers.remove(user_)

        return Response(
            {
                "isFollowing": False,
                "followCount": follower_count,
                "response": f"{user_.username} unfollowed {profile_username}",
            }
        )


class ProfileAPI(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        # print(pk)
        try:
            profile = UserProfile.objects.get(user=pk)
            user = request.user

            user_username = user.username
            str(user_username)
            if profile.user.username == user_username:
                
                UserSerializers = UserProfileSerializer(profile)
            else:
                UserSerializers = ViewUserProfileSerializer(
                    profile, context={"request": request, "pk": pk}
                )
            return Response(UserSerializers.data)
        except error:
            print(error)

    def update(self, request, pk=None):
        """
        update() is function of the Profile API, that allows users to edit their profile
        """
        try:
            user = request.user
            profile = UserProfile.objects.get(user=pk)
            # check if request is by by profile's user
            if user != profile.user:
                return HttpResponse("invalid credentials")
            else:
                serializers = ProfileEditSerializer(
                    profile, data=request.data, context={"request": request}
                )
                if serializers.is_valid():
                    serializers.save()
                # return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.data)
        except (error):
            return HttpResponse(error)


class ProfilePostsAPI(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        try:
            userProfile = UserProfile.objects.get(user=pk)
            userArticles = Article.objects.filter(author=userProfile)
            # userArticles = Article.objects.filter(author=user_)
            articleSerializer = ArticleSerializer(
                userArticles, many=True, context={"request": request}
            )

            return Response(articleSerializer.data)
        except error:
            print(error)


# Register API
#
###
class RegisterAPI(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        user = None
        data = request.data
        
        serializer = self.get_serializer(data=data)

        if serializer.is_valid(raise_exception=True):
            print(serializer.data)
            print(data )
            user = serializer.create(data)
        else:
            print("invalid data")
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

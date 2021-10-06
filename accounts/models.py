

import os
import random

# from django.db.models import Q
# from django.db.models.signals import pre_save, post_save
# from blissedmaths.utils import unique_otp_generator
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def create_user(
        self, phone, password, is_staff=False, is_active=True, is_admin=False
    ):
        if not phone:
            raise ValueError("users must have a phone number")
        if not password:
            raise ValueError("user must have a password")

        user_obj = self.model(phone=phone)
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user


class User(AbstractBaseUser):
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,14}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.",
    )
    phone = models.CharField(
        validators=[phone_regex], max_length=17, primary_key= True, unique=True
    )
    # email = models.EmailField()
    avatar = models.ImageField(
        upload_to="media/profilePictures",
        default="media/profilePictures/default-avatar.png",
    )
    
    username = models.CharField(max_length=20, blank=True, unique=True)
    standard = models.CharField(max_length=3, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    score = models.IntegerField(default=16)
    password = models.CharField(max_length=200)
    first_login = models.BooleanField(default=False)
    is_promoter = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    address = models.CharField(max_length=50, default="null", null=False)
    dob = models.CharField(max_length=8, null=False, default="00000000")
    email = models.EmailField(max_length = 254, null= True)
    has_agreed_tos = models.BooleanField(default=False)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = [
        "password",
    ]

    objects = UserManager()

    def __str__(self):
        return self.phone

    def get_full_name(self):
        return self.phone

    def get_short_name(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    #
    # when a new User object is sent to the Database create Auth token
    #
    #
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        verbose_name="user",
        related_name="profile",
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(null= True)
    avatar = models.ImageField(upload_to="media/profilePictures", default="/media/profilePictures/default-avatar.png")
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="followers",
        symmetrical=False,
    )
    instagramID = models.CharField(max_length=30, null=True, blank=True)
    snapchatID = models.CharField(max_length=30, null=True, blank=True)
    linkedinID = models.CharField(max_length=30, null=True, blank=True)
    # following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True, related_name= "following", symmetrical=False)
    # blocked = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True, related_name= "followers", symmetrical=False)
    # is_private
    def __str__(self):
        return (f"{self.user}'s Profile")


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()

    def __str__(self):
        return f"{self.user.name}'s Profile"


class FollowerRelation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(
        auto_now_add=True, null=True, blank=True
    )  # db_index = True)
    # relation = this will show us 'followed', 'unfollowed', 'blocked', etc.

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "profile"], name="unique_followers")
        ]
        ordering = ["-timestamp"]

    # def __str__(self):
    # f"{self.user} follows {self.profile}"

from django.contrib import admin
from .models import FollowerRelation, User, UserProfile


# Register your models here.
admin.site.register(UserProfile)
#admin.site.register(FollowerRelation)
@admin.register(FollowerRelation)
class FollowRelation(admin.ModelAdmin):
    list_display = ('user', 'profile', 'timestamp')

@admin.register(User)
class UserModel(admin.ModelAdmin):
    list_display = ('phone','username', 'location' )#'timestamp' )
    #list_display = ('title')
    #date_hierarchy

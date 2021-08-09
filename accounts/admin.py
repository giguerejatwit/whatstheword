from django.contrib import admin
from .models import User, UserProfile


# Register your models here.
admin.site.register(UserProfile)

@admin.register(User)
class UserModel(admin.ModelAdmin):
    list_display = ('phone', 'password' )#'timestamp' )
    #list_display = ('title')
    #date_hierarchy

from django.contrib import admin
from .models import User


# Register your models here.
#admin.site.register(Article)

@admin.register(User)
class UserModel(admin.ModelAdmin):
    list_display = ('phone', 'password' )#'timestamp' )
    #list_display = ('title')
    #date_hierarchy

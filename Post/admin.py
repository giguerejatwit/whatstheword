
from django.contrib import admin
from .models import Article


# Register your models here.
#admin.site.register(Article)

@admin.register(Article)
class ArticleModel(admin.ModelAdmin):
    list_filter = ('id','author', 'description','title', )
    #list_display = ('title')
    #date_hierarchy

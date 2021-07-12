from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from django.shortcuts import redirect

'''
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.User.objects.token.exist():
            return redirect('/wtw/articles')
        
        return view_func(request, *args, **kwargs)
    return wrapper_func
    '''
#
# 
# 
# #
def promoter_only(view_func):
        def wrapper_func(request):
            #if a user is a promoter they should be able to post.
            if request.user.is_promoter == True:
                return True
            return wrapper_func
               # group = request.user.all([0], name)
         
        return promoter_only

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
def allowed_users(allowed_rules =[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            #if request.users.groups.exists():
               # group = request.user.all([0], name)
            return  view_func(request, *args, **kwargs)
    return decorator

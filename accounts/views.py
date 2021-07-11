#from Post.decorators import unauthenticated_user
from rest_framework import generics, permissions, serializers

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .serializer import UserSerializer, RegisterSerializer
from .models import User


# Register API

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data, #in http://127.0.0.1:8000/wtw/register/ after we POST it return the context of 'fields in serializerClass
        #"token": AuthToken.objects.create(user)
        })
       



#
# registering a user
# 
# 
# #

@api_view(['POST',])
#@unauthenticated_user
def registration_view(request):

  if request.method == 'POST' :
    serializer = RegisterSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data['response'] = "succsesfully registered a new user."
        data['phone'] = account.phone
        data['password'] = account.password
        token = Token.objects.get(user =account).key
        data['token'] = token
    else:
        return Response()


#
# 
# 
# #
@api_view(['POST',])

def login_view(request):

  if request.method == 'POST' :
    serializer = RegisterSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        
        data['response'] = "succsesfully registered a new user."
        data['phone'] = account.phone
        data['password'] = account.password
        token = Token.objects.get(user =account).key
        data['token'] = token
    else:
        return Response()
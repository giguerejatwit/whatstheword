from django.core.checks.messages import ERROR
from django.db.models import query
from django.db.models.query import QuerySet
from django.http import HttpResponse, Http404, JsonResponse
from django.http.response import HttpResponseGone
from django.shortcuts import get_object_or_404, render

#allows us to authenticate tokens from knox auth
from knox.auth import TokenAuthentication
from knox.models import User #****

from rest_framework import viewsets
from rest_framework import response
from rest_framework import permissions
from rest_framework import serializers

from rest_framework.decorators import APIView, permission_classes
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status

from rest_framework import generics
from rest_framework import mixins

from .decorators import promoter_only
from .models import Article
from .serializers import ArticleSerializer

# Create your views here.
'''
class ArticleViewSet(viewsets.ModelViewSet):
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
'''

'''

class ArticleList(APIView):

    def get(self, request):
        articles = Article.objects.all()
        serializer =ArticleSerializer(articles, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer =ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status = status.HTTP_201_CREATED )
        #if error
        return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST )
    '''

'''
class ArticleList(generics.GenericAPIView, mixins.ListModelMixin,
                     mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin
):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def delete(self, request):
        return self.destroy(request)  
'''


'''
class ArticleDetails(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    def get_object(self, id):
       
        try:

            return Article.objects.get(id = id)
       
        except Article.DoesNotExist:

            return Response(status = status.HTTP_404_NOT_FOUND)
   
    
    def get(self ,request, id):
        

        article = self.get_object(id)

        serializer = ArticleSerializer(article)
        self.check_object_permissions(request, article)

        return Response(serializer.data)

    def post(self, request, id):
        
        article = self.get_object(id)
        serializer =ArticleSerializer( article, data = request.data )
        self.check_object_permissions(request, article)                 #if user is not authenticated, not posting  
        if serializer.is_valid():
                
            serializer.save()
            
            return Response(serializer.data)
        #if error
        return Response(serializer.errors,  status = status.HTTP_400_BAD_REQUEST )

    
    #
    # just like POST mthod we only want to permissions for auth is the person 
    # #
    def delete(self, request, id):
        
        article = self.get_object(id)
    
        article.delete()
    
        return (status == status.NO_CONTENT)
'''

''''''
'Using maxims make the program have less code'
''''''

'''
class ArticleDetails(generics.GenericAPIView, mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin, mixins.RetrieveModelMixin):

        queryset = Article.objects.all()
        serializer_class = ArticleSerializer

        lookup_field = 'id'

        def get(self, request, id):
            return self.retrieve(request, id = id)

        def put(self, request, id):
            return self.update(request, id=id)

        def delete(self, request, id):
            return self.destroy(request, id = id)   
'''


class ArticleViewSet(viewsets.ViewSet):
    permission_classes =(IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    #
    #anyone who is authenticated can see all. 
    # 
    # 
    # # 
    def list(self, request):
        articles = Article.objects.all()
        serializers = ArticleSerializer(articles, many = True) #bc its a QuerySet
        return Response(serializers.data)


    #
    # creating is only for is_promoter == true
    # 
    # 
    # #
    def create(self, request):
        
        article_serializer = ArticleSerializer(data = request.data)
        
           
        if article_serializer.is_valid():
            #only can create if User is a promoter
            if self.request.user.is_promoter:
                #associates the article instance to a User
                article_serializer.save(author = self.request.user)
        
            else:
                return Response('User does not have Promoter permissions')
    

            return Response(article_serializer.data, status = status.HTTP_201_CREATED)
    
        return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    #
    # anyone can retrieve but some are readOnly only if they are NOT the owner
    # 
    # 
    # #
    def retrieve(self, request, pk = None):
    
        QuerySet = Article.objects.all()
        article = get_object_or_404(QuerySet, pk=pk)
        serializers = ArticleSerializer(article)

        return Response(serializers.data)



    #
    # only Authenticated author can update
    # 
    # #
    def update(self, request, pk = None):

        article = Article.objects.get(pk = pk)
        serializer = ArticleSerializer(article, data = request.data)
        
        if serializer.is_valid():    
            serializer.save()
            return response(serializer.data, status = status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    #
    # only Authenticated author can Destroy()
    # 
    # 
    # #
    def destroy(self, request, pk = None):
        article = Article.objects.get(pk = pk)
        article.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)

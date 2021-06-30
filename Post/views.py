from django.core.checks.messages import ERROR
from django.db.models import query
from django.db.models.query import QuerySet
from django.http import HttpResponse, Http404, JsonResponse
from django.http.response import HttpResponseGone
from django.shortcuts import get_object_or_404, render
import rest_framework
from rest_framework import viewsets
from rest_framework import response

from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

from rest_framework import generics
from rest_framework import mixins


from .models import Article
from .serializers import ArticleSerializer






# Create your views here.
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




class ArticleDetails(APIView):
    
    def get_object(self, id):
       
        try:

            return Article.objects.get(id = id)
       
        except Article.DoesNotExist:

            return Response(status = status.HTTP_404_NOT_FOUND)

    def get(self ,request, id):
        
        article = self.get_object(id)

        serializer = ArticleSerializer(article)

        return Response(serializer.data)

    def post(self, request, id):
        
        article = self.get_object(id)
        serializer =ArticleSerializer( article, data = request.data )

        if serializer.is_valid():
                
            serializer.save()
            
            return Response(serializer.data)
        #if error
        return Response(serializer.errors,  status = status.HTTP_400_BAD_REQUEST )

    def delete(self, request, id):
        
        article = self.get_object(id)
        article.delete()
        
        return (status == status.NO_CONTENT)



'Using maxims make the program have less code'

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

'''
class ArticleViewSet(viewsets.ViewSet):

    def list(self, request):
        articles = Article.objects.all()
        serializers = ArticleSerializer(articles, many = True) #bc its a QuerySet
        return Response(serializers.data)

    def create(self, request):
        serializer = ArticleSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return response(serializer.data, status = status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk = None):
    
        QuerySet = Article.objects.all()
        article = get_object_or_404(QuerySet, pk=pk)
        serializers = ArticleSerializer(article)

        return Response(serializers.data)

    def update(self, request, pk = None):

        article = Article.objects.get(pk = pk)
        serializer = ArticleSerializer(article, data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return response(serializer.data, status = status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def destroy(self, request, pk = None):
        article = Article.objects.get(pk = pk)
        article.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)

'''

class ArticleViewSet(viewsets.ModelViewSet):
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

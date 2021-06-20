from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status


from .models import Article
from .serializers import ArticleSerializer

# Create your views here.

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


class ArticleDetails(APIView):
    
    def get_object(self, id):
        try:
            return Article.object.get(id = id)
        except Article.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

    def get(self ,request, id):
        articles =self.get_object
        serializer =ArticleSerializer(articles)
        return Response(serializer.data)

    def put(self, request, id):
        articles = self.get_object(id)
        serializer =ArticleSerializer( articles, data = request.data )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        #if error
        return Response(serializer.errors,  status = status.HTTP_400_BAD_REQUEST )

    def delete(self, request, id):
        article = self.get_object(id)
        article.delete()
        return (status == status.NO_CONTENT)
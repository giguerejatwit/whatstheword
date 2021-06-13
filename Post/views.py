from django.shortcuts import render, HttpResponse

# Create your views here.

def Index(req):
    return HttpResponse("I LOVE Kishu")
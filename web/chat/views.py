from django.http import HttpResponse

def index(request):
    return HttpResponse("GRAiS chat app is running")

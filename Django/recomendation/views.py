from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello world!")

def results(request, playerId):
    return HttpResponse("Player id: " + str(playerId))

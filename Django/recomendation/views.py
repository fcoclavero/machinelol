from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import LasUser

# Create your views here.
def index(request):
    return HttpResponse("Hello world!")

def results(request, playerId):
    latestUserList = LasUser.objects.order_by('-registrationDate')[:5]
    template = loader.get_template('recomendation/index.html')
    context = {
        'latestUserList' : latestUserList,
        'receivedId' : playerId,
    }
    return HttpResponse(template.render(context, request))

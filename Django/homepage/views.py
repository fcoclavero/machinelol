from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    template = loader.get_template('homepage/index.html')
    context = {
        'regions' : ["br", "eune", "euw", "kr", "lan", "las", "na", "oce", "ru", "tr"],
    }
    return HttpResponse(template.render(context, request))

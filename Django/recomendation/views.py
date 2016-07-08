from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import User

# Create your views here.
def recomendation(request):
    # latestUserList = User.objects.order_by('-registrationDate')[:5]
    template = loader.get_template('recomendation/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

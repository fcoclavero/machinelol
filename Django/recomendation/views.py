from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import LasUser
from .forms import SignInForm

from recomendation.utilities import *

# Create your views here.
def recomendation(request):
    if request.method == 'POST':
        # Five champions to test display
        champions = (79,222,268,105,201)

        # Create form instance and populate with data in the request
    latestUserList = LasUser.objects.order_by('-registrationDate')[:5]

        print(request.POST.get('summo'))
        print(request.POST.get('region'))

        # Check validity
        if form.is_valid():
            data = form.cleaned_data

            id = getId(data["summonerName"], data["region"])

            if id == False:
                return render(request, 'recomendation/error.html', {'message':"invalid summoner name"})
            else:
                return render(request, 'recomendation/index.html', {'summonerName':data['summonerName'], 'region':data['region'], 'id':id, 'champions':[getChampionData(data['region'], x) for x in champions]})

        # If invalid redirect to error page
        else:
            return render(request, 'recomendation/error.html', {'message':"invalid form"})
    else:
        return render(request, 'recomendation/error.html', {'message':"request not post"})

import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import SignInForm

from recomendation.utilities import *

# Create your views here.
def recomendation(request):
    if request.method == 'POST':
        print(request.POST.get('summonerName'))
        print(request.POST.get('region'))

        # create a form instance and populate it with data from the request:
        form = SignInForm(request.POST)

        # Check validity
        if form.is_valid():
            data = form.cleaned_data

            id = getId(data["summonerName"], data["region"])

            if id == False:
                return render(request, 'recomendation/error.html', {'message':"invalid summoner name"})
            else:
                return render(request, 'recomendation/index.html', {'summonerName':data['summonerName'], 'region':data['region'], 'id':id})

        # If invalid redirect to error page
        else:
            return render(request, 'recomendation/error.html', {'message':"invalid form"})
    else:
        return render(request, 'recomendation/error.html', {'message':"request not post"})

def ajax(request):
    print('Recomendation request')

    playerId = request.POST.get('playerId')
    region = request.POST.get('region')

    if playerId is None or region is None:
        return render(request, 'recomendation/error.html', {'message':"missing parameter"})

    # Add only top hits to recomendation view
    recomendation = getRecomendation(playerId = playerId, playerRegion = region)
    for key, value in recomendation.items():
        print(key)
        print(value)

        # Keep only top 5 champions
        recomendation[key] = [getChampionData(region, championId) for championId in value[0:5]]

    return HttpResponse(json.dumps(recomendation))

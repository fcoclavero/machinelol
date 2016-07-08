from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import User
from .forms import SignInForm

import requests, json

keys = ["9b25bbda-7da3-4ee5-9d6b-a7ff2c402c0d", "0b808dbd-c044-43db-88a0-829dbd390aa7"]

def getId(summonerName, region):
    data = requests.get("https://las.api.pvp.net/api/lol/" + region + "/v1.4/summoner/by-name/" + summonerName + "?api_key=" + keys[0])

    # TODO: manage name not found
    return data.json()[summonerName]['id']

# Create your views here.
def recomendation(request):
    if request.method == 'POST':
        # Create form instance and populate with data in the request
        form = SignInForm(request.POST)

        # Check validity
        if form.is_valid():
            data = form.cleaned_data
            return render(request, 'recomendation/index.html', {'summonerName':data['summonerName'], 'region':data['region'], 'id':getId(data["summonerName"], data["region"])})

        # If invalid redirect to error page
        else:
            return render(request, 'recomendation/error.html', {'message':"invalid form"})
    else:
        return render(request, 'recomendation/error.html', {'message':"request not post"})

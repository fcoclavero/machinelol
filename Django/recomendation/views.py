from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import User
from .forms import SignInForm

from recomendation.utilities import *

# Create your views here.
def recomendation(request):
    if request.method == 'POST':
        # Create form instance and populate with data in the request
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

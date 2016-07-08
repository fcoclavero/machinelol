from django import forms

class SignInForm(forms.Form):
    summonerName = forms.CharField(label="Summoner name", max_length=200)
    region = forms.CharField(label="Region", max_length=4)

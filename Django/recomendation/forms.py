from django import forms

class SignInForm(forms.Form):
    summonerName = forms.CharField(label="summonerName", max_length=200)
    region = forms.CharField(label="region", max_length=4)

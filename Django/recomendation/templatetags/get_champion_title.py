import requests

from django import template
from django.template.defaulttags import register

register = template.Library()

keys = ["9b25bbda-7da3-4ee5-9d6b-a7ff2c402c0d", "0b808dbd-c044-43db-88a0-829dbd390aa7"]

@register.filter
def get_champion_title(region, id):
    data = requests.get("https://las.api.pvp.net/api/lol/static-data/" + region + "/v1.2/champion/" + str(id) + "?api_key=" + keys[0])
    return data.json()['title']

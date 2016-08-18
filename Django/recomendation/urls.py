from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.recomendation, name='recomendation'),
    url(r'^(?P<playerId>[0-9]+)&(?P<region>[0-9]+)/$', views.getRecomendation, name='getRecomendation'), # results via get
]

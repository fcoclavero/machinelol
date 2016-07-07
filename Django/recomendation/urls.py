from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='recomendation_index'),
    url(r'^(?P<playerId>[0-9]+)/$', views.results, name='recomendation'),
]

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<playerId>[0-9]+)/$', views.results, name='results'),
]

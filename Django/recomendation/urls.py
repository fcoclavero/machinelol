from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^', views.recomendation, name='recomendation'),
    # url(r'^(?P<playerId>[0-9]+)/$', views.recomendation, name='recomendation'), # results vía get
]

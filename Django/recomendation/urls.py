from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.recomendation, name='recomendation'),
    url(r'^ajax/$', views.ajax, name='ajax'), # results via get
]

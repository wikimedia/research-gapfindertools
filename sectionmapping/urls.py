from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, {
        "template_name": "sectionmapping/index.html"
    }, name='index'),
    path('map', views.mapping, {
        "template_name": "sectionmapping/map.html"
    }, name='map')
]

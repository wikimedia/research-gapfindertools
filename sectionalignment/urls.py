from django.urls import path

from . import views

app_name = 'sectionalignment'

urlpatterns = [
    path('', views.index, {
        "template_name": "sectionalignment/index.html"
    }, name='index'),
    path('mapping', views.mapping, {
        "template_name": "sectionalignment/mapping.html"
    }, name='mapping'),
    path('mapping/save', views.save_mapping, name='save_mapping')
]

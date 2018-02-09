from django.shortcuts import render
from django.http import HttpResponse

# from . import models
from . import forms


def index(request):
    if request.session.get('wp-username'):
        return HttpResponse("Hello, %s." % request.session.get('wp-username'))
    else:
        return render(request, "index.html", {
            'translator_form': forms.TranslatorForm()
        })

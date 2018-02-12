from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# from . import models
from . import forms


def index(request):
    # del request.session['mapper']
    if request.method == 'POST':
        form = forms.MapperForm(request.POST)
        if form.is_valid():
            new_mapper = form.save()
            # TODO: obfuscate
            request.session['mapper'] = new_mapper.id
            return HttpResponseRedirect('translate')
    else:
        if request.session.get('mapper'):
            return HttpResponseRedirect('translate')
        else:
            form = forms.MapperForm()

    return render(request, "index.html", {
        'form': form
    })


def translate(request):
    return HttpResponse('translate page')

import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import Mapper, Mapping, Section, MappingSummary
from .forms import MapperForm


def index(request):
    # del request.session['mapper']
    if request.method == 'POST':
        form = MapperForm(request.POST)
        if form.is_valid():
            new_mapper = form.save()
            request.session['mapper'] = new_mapper.id
            return HttpResponseRedirect('map')
    else:
        if request.session.get('mapper'):
            return HttpResponseRedirect('map')
        else:
            form = MapperForm()

    return render(request, "index.html", {
        'form': form
    })


def mapping(request):
    if not request.session['mapper']:
        return HttpResponseRedirect('index')
    try:
        mapper = Mapper.objects.get(id=request.session['mapper'])
    except ObjectDoesNotExist:
        return HttpResponseRedirect('index')

    source_language = mapper.get_source_language()
    target_languages = mapper.get_target_languages()
    print(source_language)
    print(target_languages)
    if not source_language or not target_languages:
        return HttpResponse(
            "Sorry, we don't have any data for you at this time.")

    mapping_summary = MappingSummary.objects.filter(
        source__language=source_language).first()
    if not mapping_summary:
        return HttpResponse("No data at this time.")

    targets = json.loads(mapping_summary.source.targets)
    questions = {language: targets[language] for language in target_languages}
    print(questions)

    return render(request, "map.html", {
        'mapper': mapper,
        'source': mapping_summary.source.title,
        'questions': questions
    })

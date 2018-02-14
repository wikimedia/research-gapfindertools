import json
from random import shuffle

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Mapper, Mapping, Section, MappingSummary, LANGUAGE_CHOICES
from .forms import MapForm, MapperForm


LANGUAGE_CHOICES_DICT = dict(LANGUAGE_CHOICES)


def index(request):
    # del request.session['mapper']
    if request.method == 'POST':
        form = MapperForm(request.POST)
        if form.is_valid():
            new_mapper = form.save()
            request.session['mapper'] = new_mapper.id
            return HttpResponseRedirect(reverse('map'))
    else:
        if request.session.get('mapper'):
            return HttpResponseRedirect(reverse('map'))
        else:
            form = MapperForm()

    return render(request, "index.html", {
        'form': form
    })


def mapping(request):
    # TODO: decorate
    if 'mapper' not in request.session:
        return HttpResponseRedirect(reverse('index'))
    try:
        mapper = Mapper.objects.get(id=request.session['mapper'])
    except ObjectDoesNotExist:
        del request.session['mapper']
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        language = request.POST.get('language')
        title = request.POST.get('title')
        if not language or not title:
            return HttpResponseRedirect(reverse('index'))
        section = Section.objects\
                         .filter(language=language, title=title)\
                         .first()
        if not section:
            return HttpResponseRedirect(reverse('index'))

        targets = {}
        ar = request.POST.getlist('ar')
        if ar:
            targets['ar'] = ar
        en = request.POST.getlist('en')
        if en:
            targets['en'] = en
        es = request.POST.getlist('es')
        if es:
            targets['es'] = es
        fr = request.POST.getlist('fr')
        if fr:
            targets['fr'] = fr
        ja = request.POST.getlist('ja')
        if ja:
            targets['ja'] = ja
        ru = request.POST.getlist('ru')
        if ru:
            targets['ru'] = ru

        targets = {
            lang: [value for value in values if value.strip()]
            for lang, values in targets.items()
        }

        new_mapping = Mapping(mapper=mapper,
                              source=section,
                              targets=json.dumps(targets, ensure_ascii=False))
        new_mapping.save()
        return HttpResponseRedirect(reverse('map'))
    else:
        source_language = mapper.get_source_language()
        target_languages = mapper.get_target_languages()
        if not source_language or not target_languages:
            return HttpResponse(
                "Sorry, we don't have any data for you at this time.")

        user_mappings = Mapping.objects.filter(mapper=mapper)\
                                       .values("source__id")
        mapping_summary = MappingSummary.objects\
                                        .filter(source__language=source_language)
        if user_mappings:
            mapping_summary = mapping_summary\
                              .exclude(source__id__in=user_mappings)
        mapping_summary = mapping_summary.first()

        if not mapping_summary:
            return HttpResponse("No data at this time.")

        targets = json.loads(mapping_summary.source.targets)
        # TODO: make ordered dict
        questions = {}
        for lang_code in target_languages:
            shuffle(targets[lang_code])
            questions[lang_code] = {
                'language': LANGUAGE_CHOICES_DICT[lang_code],
                'targets': targets[lang_code]
            }

        return render(request, "map.html", {
            'mapper': mapper,
            'title': mapping_summary.source.title,
            'language': mapping_summary.source.language,
            'questions': questions
        })

import json
from random import shuffle

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, UserMapping, ModelMapping, UserMappingSummary,\
    LANGUAGE_CHOICES
from .forms import UserForm


LANGUAGE_CHOICES_DICT = dict(LANGUAGE_CHOICES)


def index(request, template_name):
    # del request.session['user-id']
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            request.session['user-id'] = new_user.id
            return HttpResponseRedirect(reverse('sectionalignment:mapping'))
    else:
        change_user_data = request.GET.get('change', None)
        user_id = request.session.get('user-id', None)
        if user_id and not change_user_data:
            return HttpResponseRedirect(reverse('sectionalignment:mapping'))
        form = UserForm()

    return render(request, template_name, {
        'form': form
    })


def mapping(request, template_name):
    # TODO: decorate
    user_id = request.session.get('user-id', None)
    user = None
    if user_id:
        user = User.objects.filter(id=user_id).first()
        if not user:
            del request.session['user-id']
    if not user:
        return HttpResponseRedirect(reverse('sectionalignment:index'))

    if request.method == 'POST':
        language = request.POST.get('language')
        title = request.POST.get('title')
        if not language or not title:
            return HttpResponseRedirect(reverse('sectionalignment:index'))
        section = ModelMapping.objects\
                              .filter(section_language=language,
                                      section_title=title)\
                              .first()
        if not section:
            return HttpResponseRedirect(reverse('sectionalignment:index'))

        mappings = {}
        ar = request.POST.getlist('ar')
        if ar:
            mappings['ar'] = ar
        en = request.POST.getlist('en')
        if en:
            mappings['en'] = en
        es = request.POST.getlist('es')
        if es:
            mappings['es'] = es
        fr = request.POST.getlist('fr')
        if fr:
            mappings['fr'] = fr
        ja = request.POST.getlist('ja')
        if ja:
            mappings['ja'] = ja
        ru = request.POST.getlist('ru')
        if ru:
            mappings['ru'] = ru

        mappings = {
            lang: [value for value in values if value.strip()]
            for lang, values in mappings.items()
        }

        new_mapping = UserMapping(mapper=user,
                                  source=section,
                                  mappings=json.dumps(mappings, ensure_ascii=False))
        new_mapping.save()
        return HttpResponseRedirect(reverse('sectionalignment:mapping'))
    else:
        source_language = user.get_source_language()
        target_languages = user.get_target_languages()
        if not source_language or not target_languages:
            return HttpResponse(
                "Sorry, we don't have any data for you at this time.")

        user_mappings = UserMapping.objects.filter(mapper=user)\
                                           .values("source__id")
        mapping_summary = UserMappingSummary.objects .filter(
            source__section_language=source_language
        )
        if user_mappings:
            mapping_summary = mapping_summary\
                              .exclude(source__id__in=user_mappings)
        mapping_summary = mapping_summary.first()

        if not mapping_summary:
            return HttpResponse("No data at this time.")

        mappings = json.loads(mapping_summary.source.mappings)
        # TODO: make ordered dict
        questions = {}
        for lang_code in target_languages:
            shuffle(mappings[lang_code])
            questions[lang_code] = {
                'language': LANGUAGE_CHOICES_DICT[lang_code],
                'mappings': mappings[lang_code]
            }
        print(questions)

        return render(request, template_name, {
            'user': user,
            'title': mapping_summary.source.section_title,
            'language': mapping_summary.source.section_language,
            'questions': questions
        })

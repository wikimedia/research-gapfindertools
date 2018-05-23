from datetime import datetime
# import json
# from random import shuffle
# import time

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Mapping, UserInput, LANGUAGE_CHOICES


LANGUAGE_CHOICES_DICT = dict(LANGUAGE_CHOICES)


def index(request, template_name):
    # del request.session['user']
    source = request.GET.get('s')
    destination = request.GET.get('d')
    change_user_data = request.GET.get('c')

    if source in LANGUAGE_CHOICES_DICT and\
       destination in LANGUAGE_CHOICES_DICT and\
       source != destination:
        request.session['user'] = {
            'source': source,
            'destination': destination
        }
        return HttpResponseRedirect(reverse('sectionalignment:mapping'))
    elif request.session.get('user') and not change_user_data:
        return HttpResponseRedirect(reverse('sectionalignment:mapping'))

    return render(request, template_name)


def mapping(request, template_name):
    user = request.session.get('user')
    if not user:
        return HttpResponseRedirect(reverse('sectionalignment:index'))

    question = request.session.get('question')

    if question and request.method == 'POST':
        if 'skip' in request.POST:
            user['skipped'].append(question['id'])
        elif 'save' in request.POST:
            pass
            # mapping = Mapping.objects.get(pk=question['id'])
        # save
        return HttpResponseRedirect(reverse('sectionalignment:mapping'))
    else:
        # autocomplete suggestions
        suggestions = Mapping.objects\
                             .filter(language=user['destination'])\
                             .values_list('title', flat=True)

        user_input = None
        # has the user refreshed the page?
        if question:
            user_input = UserInput.objects.filter(
                id=question['id'],
                done=False
            ).first()

        if not user_input:
            user_input = UserInput.objects.filter(
                source__language=user['source'],
                destination_language=user['destination'],
                done=False
            ).order_by('source__rank').first()

        request.session['question'] = {
            'id': user_input.id
        }

        return render(request, template_name, {
            'source_language': LANGUAGE_CHOICES_DICT[user['source']],
            'destination_language': LANGUAGE_CHOICES_DICT[user['destination']],
            'user': user,
            'user_input': user_input,
            'suggestions': list(suggestions)
        })

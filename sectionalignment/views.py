# TODO show error if source and destination languages are not valid
# TODO show error if user input is empty and they didn't skip but saved it
# TODO when user goes back to index, drop their question, and put back
# their question timestamp so other can take it

from datetime import datetime, timedelta
# import json
# from random import shuffle
# import time

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Mapping, UserInput, LANGUAGE_CHOICES


LANGUAGE_CHOICES_DICT = dict(LANGUAGE_CHOICES)


def clear_user_session(request):
    if 'user' in request.session:
        del request.session['user']

    if 'question' in request.session:
        # free the question for others to answer
        user_input = UserInput.objects.get(
            id=request.session['question']['id']
        )
        user_input.start_time = datetime.now() - timedelta(minutes=10)
        user_input.save()
        del request.session['question']


def index(request, template_name):
    source = request.GET.get('s')
    destination = request.GET.get('d')
    change_user_data = request.GET.get('c')

    if source in LANGUAGE_CHOICES_DICT and\
       destination in LANGUAGE_CHOICES_DICT and\
       source != destination:
        clear_user_session(request)
        request.session['user'] = {
            'source': source,
            'destination': destination,
            'skipped': []
        }
        return HttpResponseRedirect(reverse('sectionalignment:mapping'))
    elif request.session.get('user') and not change_user_data:
        clear_user_session(request)
        return HttpResponseRedirect(reverse('sectionalignment:mapping'))

    return render(request, template_name)


def mapping(request, template_name):
    user = request.session.get('user')
    if not user:
        return HttpResponseRedirect(reverse('sectionalignment:index'))

    question = request.session.get('question')
    if question and request.method == 'POST':
        if 'skip' in request.POST:
            # use set instead of list
            user['skipped'].append(question['id'])
        elif 'save' in request.POST:
            # TODO handle cases when this is already saved, skip maybe?
            translation = request.POST.get('translation', '').strip()
            if translation:
                user_input = UserInput.objects.get(pk=question['id'])
                user_input.destination_title = translation
                user_input.done = True
                user_input.save()
                user['counter'] = user.get('counter', 0) + 1
        request.session['user'] = user
        request.session['question'] = None
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
                source__language=user['source'],
                destination_language=user['destination'],
                id=question['id'],
                done=False
            ).first()

        if not user_input:
            user_input = UserInput.objects.filter(
                source__language=user['source'],
                destination_language=user['destination'],
                done=False,
                start_time__lt=datetime.now() - timedelta(minutes=5)
            ).exclude(id__in=user['skipped']).order_by('source__rank').first()
            # save start time so someone else doesn't take the same question
            if user_input:
                user_input.start_time = datetime.now()
                user_input.save()

        request.session['question'] = {
            'id': user_input.id
        }

        request.session['user'] = user

        print('user')
        print(user)
        print('question')
        print(question)

        return render(request, template_name, {
            'source_language': LANGUAGE_CHOICES_DICT[user['source']],
            'destination_language': LANGUAGE_CHOICES_DICT[user['destination']],
            'user': user,
            'user_input': user_input,
            'suggestions': list(suggestions)
        })

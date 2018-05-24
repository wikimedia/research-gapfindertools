# TODO show error if source and destination languages are not valid
# TODO show error if user input is empty and they didn't skip but saved it
# TODO when user goes back to index, drop their question, and put back
# their question timestamp so other can take it

from datetime import datetime, timedelta
import json
# from random import shuffle
# import time

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

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


@require_GET
def index(request, template_name):
    """Index page
    - If 'c' GET parameter is set, clear session data and allow
      selecting languages.
    - Else if 's' (source) and 'd' (destination) are passed and
      distinct valid LANGUAGE_CHOICES, then redirect to /mapping.
    - Else if user session is already present, redirect to /mapping.
    """
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
        return HttpResponseRedirect(reverse('sectionalignment:mapping'))

    clear_user_session(request)
    return render(request, template_name)


@require_POST
def save_mapping(request):
    """Save mapping
    """
    user = request.session.get('user')
    question = request.session.get('question')
    if not user or not question:
        return HttpResponseRedirect(reverse('sectionalignment:mapping'))

    if 'skip' in request.POST:
        user['skipped'].append(question['id'])
    elif 'save' in request.POST:
        translation = request.POST.getlist('translation', [])
        translation_set = {t.strip() for t in translation if t.strip()}
        # add entry to the skipped list if no input is provided
        if not len(translation_set):
            user['skipped'].append(question['id'])
        else:
            user_input = UserInput.objects.get(pk=question['id'])
            # this should not happen, but in case data is already there,
            # append.
            if user_input.done:
                translation_set |= set(
                    json.loads(user_input.destination_title or '')
                )
            user_input.destination_title = json.dumps(
                list(translation_set))
            user_input.done = True
            user_input.save()
            user['counter'] = user.get('counter', 0) + 1
    request.session['user'] = user
    request.session['question'] = None
    return HttpResponseRedirect(reverse('sectionalignment:mapping'))


@require_GET
def mapping(request, template_name):
    """Show a question
    - If no user session is present, redirect to /index.
    - Else if the user refreshed the page, show the old question.
    - Else show a new question, but only if it hasn't been seen in the
      last 5 minutes
    - Then update the question's start_time to now(), and set session
      values.
    """
    user = request.session.get('user')
    if not user:
        return HttpResponseRedirect(reverse('sectionalignment:index'))

    user_input = None

    question = request.session.get('question')
    # Has the user refreshed the page?
    if question:
        user_input = UserInput.objects.filter(
            id=question['id'],
            source__language=user['source'],
            destination_language=user['destination'],
            done=False
        ).first()

    # Nope, the user is asking for a new question.
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

    # autocomplete suggestions
    suggestions = Mapping.objects\
                         .filter(language=user['destination'])\
                         .values_list('title', flat=True)

    return render(request, template_name, {
        'source_language': LANGUAGE_CHOICES_DICT[user['source']],
        'destination_language': LANGUAGE_CHOICES_DICT[user['destination']],
        'user': user,
        'user_input': user_input,
        'suggestions': list(suggestions)
    })

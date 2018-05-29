from datetime import datetime, timedelta
import json

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from .models import Mapping, UserInput, LANGUAGE_CHOICES


LANGUAGE_CHOICES_DICT = dict(LANGUAGE_CHOICES)


def set_new_user_session(request, source=None, destination=None):
    """Create request.session['user']."""
    user = {
        'source': source,
        'destination': destination,
        'progress': 0
    }
    for s, _ in LANGUAGE_CHOICES:
        user[s] = {}
        for d, _ in LANGUAGE_CHOICES:
            if s == d:
                continue
            user[s][d] = {
                'skipped': [],
                'question': None
            }
    request.session['user'] = user
    request.session.modified = True


def get_user_session(request):
    """Return user data from request.session."""
    return request.session.get('user')


def set_user_session_languages(request, source, destination):
    """Set user's source and destination languages."""
    user = request.session['user']
    user['source'] = source
    user['destination'] = destination
    request.session['user'] = user
    request.session.modified = True


def set_user_session_skipped(request,  skipped):
    """Add skipped to the list of skipped questions for source and
    destionation."""
    user = request.session['user']
    source = user['source']
    destination = user['destination']
    user[source][destination]['skipped'].append(skipped)
    request.session['user'] = user
    request.session.modified = True


def increase_user_session_progress(request):
    """Add 1 to user's progress for source and destination."""
    request.session['user']['progress'] += 1
    request.session.modified = True


def set_user_session_question(request, id):
    """Set current question ID."""
    user = request.session['user']
    source = user['source']
    destination = user['destination']
    user[source][destination]['question'] = id
    request.session['user'] = user
    request.session.modified = True


def get_user_session_question(request):
    """Return the current question ID."""
    user = request.session['user']
    source = user['source']
    destination = user['destination']
    return user[source][destination]['question']


def delete_user_session_question(request):
    """Delete question from user session."""
    user = request.session['user']
    source = user['source']
    destination = user['destination']
    user[source][destination]['question'] = None
    request.session['user'] = user
    request.session.modified = True


@require_GET
def index(request, template_name):
    """Index page
    - If 'c' GET parameter is set, clear user languages and question
      data and allow selecting languages.
    - Else if 's' (source) and 'd' (destination) are passed and
      distinct valid LANGUAGE_CHOICES, then redirect to /mapping.
    - Else if user session is already present, redirect to /mapping.
    """
    # del request.session['user']
    # request.session.modified = True
    # return HttpResponse(request.session)
    user = get_user_session(request)
    source = request.GET.get('s')
    destination = request.GET.get('d')

    if source in LANGUAGE_CHOICES_DICT and\
       destination in LANGUAGE_CHOICES_DICT and\
       source != destination:
        if user:
            set_user_session_languages(request, source, destination)
        else:
            set_new_user_session(request, source, destination)
        return HttpResponseRedirect(reverse('sectionalignment:mapping'))

    if user and not request.GET.get('c'):
        return HttpResponseRedirect(reverse('sectionalignment:mapping'))

    return render(request, template_name)


@require_POST
def save_mapping(request):
    """Save mapping
    """
    user = get_user_session(request)
    question = get_user_session_question(request)
    if not user or not question:
        return HttpResponseRedirect(reverse('sectionalignment:mapping'))

    if 'skip' in request.POST:
        set_user_session_skipped(request, question)
    elif 'save' in request.POST:
        translation = request.POST.getlist('translation', [])
        translation_set = {t.strip() for t in translation if t.strip()}
        # add entry to the skipped list if no input is provided
        if not len(translation_set):
            set_user_session_skipped(request, question)
        else:
            user_input = UserInput.objects.get(pk=question)
            # this should not happen, but in case data is already there,
            # append.
            if user_input.done:
                translation_set |= set(
                    json.loads(user_input.destination_title or '')
                )
            user_input.destination_title = json.dumps(
                list(translation_set), ensure_ascii=False)
            user_input.done = True
            user_input.user_session_key = request.session.session_key
            user_input.save()
            increase_user_session_progress(request)

    # we're done with this question
    delete_user_session_question(request)

    return HttpResponseRedirect(reverse('sectionalignment:mapping'))


@require_GET
def mapping(request, template_name):
    """Show a question
    - If no user session is present, redirect to /index.
    - Else if the user refreshed the page, show the old question.
    - Else show a new question, but only if it hasn't been seen in the
      last QUESTION_DROP_MINUTES minutes.
    - Then update the question's start_time to now(), and set session
      values.
    """
    user = get_user_session(request)
    if not user:
        return HttpResponseRedirect(reverse('sectionalignment:index'))

    source = user['source']
    destination = user['destination']
    user_input = None
    question = get_user_session_question(request)

    # Has the user refreshed the page?
    if question:
        user_input = UserInput.objects.filter(
            id=question,
            source__language=user['source'],
            destination_language=user['destination'],
            done=False
        ).first()

    # Nope, the user is asking for a new question.
    if not user_input:
        user_input = UserInput.objects.filter(
            source__language=source,
            destination_language=destination,
            done=False,
            start_time__lt=datetime.now() - timedelta(
                minutes=settings.QUESTION_DROP_MINUTES)
        ).exclude(
            id__in=user[source][destination]['skipped']
        ).order_by('source__rank').first()

    # save start time so someone else doesn't take the same question
    if user_input:
        user_input.start_time = datetime.now()
        user_input.user_session_key = request.session.session_key
        user_input.save()
        set_user_session_question(request, user_input.id)

    # autocomplete suggestions
    suggestions = Mapping.objects\
                         .filter(language=user['destination'])\
                         .values_list('title', flat=True)

    return render(request, template_name, {
        'source': {
            'code': user['source'],
            'title': LANGUAGE_CHOICES_DICT[user['source']]
        },
        'destination': {
            'code': user['destination'],
            'title': LANGUAGE_CHOICES_DICT[user['destination']]
        },
        'user': user,
        'user_input': user_input,
        'suggestions': list(suggestions),
        'language_choices_dict': LANGUAGE_CHOICES_DICT
    })

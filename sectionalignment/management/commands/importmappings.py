import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from openpyxl import load_workbook

from sectionalignment.models import Mapping, UserInput, LANGUAGE_CHOICES


class Command(BaseCommand):
    help = 'Imports model generated data into database'

    def add_arguments(self, parser):
        parser.add_argument('workbook', nargs=1, type=str)

    def handle(self, *args, **options):
        print("Started importing data ...")
        workbook = load_workbook(options['workbook'][0])
        for source_lang, _ in LANGUAGE_CHOICES:
            for destination_lang, _ in LANGUAGE_CHOICES:
                if source_lang == destination_lang:
                    continue
                # if source_lang != 'en' or destination_lang != 'es':
                    # continue
                sheet = workbook['%s%s' % (source_lang, destination_lang)]
                for i, row in enumerate(sheet.rows):
                    # print([x.value for x in row])
                    # handle duplicates
                    mapping = Mapping.objects.filter(
                        title=str(row[0].value),
                        language=source_lang,
                    ).first()
                    if not mapping:
                        mapping = Mapping(
                            title=str(row[0].value),
                            language=source_lang,
                            rank=i)
                        mapping.save()

                    # update duplicates
                    user_inputs_from_sheet = [str(x.value)
                                              for x in row[1:] if x.value]
                    user_input = UserInput.objects.filter(
                        source=mapping,
                        destination_language=destination_lang
                    ).first()
                    if user_input:
                        if user_inputs_from_sheet:
                            user_input.destination_title = json.dumps(
                                user_inputs_from_sheet +
                                json.loads(
                                    user_input.destination_title
                                ),
                                ensure_ascii=False
                            )
                            user_input.done = True
                            user_input.save()
                    # otherwise create new
                    else:
                        user_input = UserInput(
                            source=mapping,
                            destination_language=destination_lang,
                            destination_title=json.dumps(
                                user_inputs_from_sheet,
                                ensure_ascii=False
                            ),
                            done=len(user_inputs_from_sheet) > 0,
                            # So that questions appear immediately (because
                            # the cut off time is QUESTION_DROP_MINUTES).
                            start_time=timezone.now() - timezone.timedelta(
                                minutes=(settings.QUESTION_DROP_MINUTES + 1))
                        )
                        user_input.save()
                self.stdout.write(
                    'Done with %s-%s.' % (source_lang, destination_lang))
        self.stdout.write('Import done.')

from django.core.management.base import BaseCommand, CommandError
from sectionmapping.models import Section, LANGUAGE_CHOICES
import json


class Command(BaseCommand):
    help = 'Imports model generated data into database'

    def add_arguments(self, parser):
        parser.add_argument('json_filename', nargs=1, type=str)
        parser.add_argument('language', nargs=1, type=str)

    def handle(self, *args, **options):
        # TODO: update when data is line by line
        with open(options['json_filename'][0], 'r', encoding='utf-8') as json_file:
            language = options['language'][0]
            json_data = json.loads(json_file.read())
            for title, data in json_data.items():
                targets = {}
                for language_choice in dict(LANGUAGE_CHOICES).keys():
                    if language_choice != language:
                        if language_choice in data:
                            targets[language_choice] = data[language_choice]
                        else:
                            print("%s is missing %s mappings." % (title, language_choice))
                targets = json.dumps(targets, ensure_ascii=False)
                section = Section(title=title, language=language,
                                  rank=data['rank'], targets=targets)
                section.save()
            self.stdout.write('Import done.')

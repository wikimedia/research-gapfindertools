from django.core.management.base import BaseCommand, CommandError
from sectionalignment.models import ModelMapping, LANGUAGE_CHOICES
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
            count = 0
            for title, data in json_data.items():
                if count > 5:
                    return
                count += 1
                mappings = {}
                for language_choice in dict(LANGUAGE_CHOICES).keys():
                    if language_choice != language:
                        if language_choice in data:
                            mappings[language_choice] = data[language_choice]
                        else:
                            print("%s is missing %s mappings." % (title, language_choice))
                mappings = json.dumps(mappings, ensure_ascii=False)
                section = ModelMapping(section_title=title,
                                       section_language=language,
                                       section_rank=data['rank'],
                                       mappings=mappings)
                section.save()
            self.stdout.write('Import done.')

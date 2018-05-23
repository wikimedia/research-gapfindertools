import csv

from django.core.management.base import BaseCommand
from sectionalignment.models import Mapping, UserInput, LANGUAGE_CHOICES


class Command(BaseCommand):
    help = 'Imports model generated data into database'

    def add_arguments(self, parser):
        parser.add_argument('tsv_filename', nargs=1, type=str)

    def handle(self, *args, **options):
        # TODO: update when data is line by line
        print("Starting to import.")
        with open(options['tsv_filename'][0], 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile, delimiter='\t', quotechar='"')
            for i, row in enumerate(reader):
                row = [x.strip() for x in row]
                entries = []
                if row[0]:
                    entries.append(Mapping(
                        title=row[0],
                        language='ar',
                        rank=i))
                if row[1]:
                    entries.append(Mapping(
                        title=row[1],
                        language='en',
                        rank=i))
                if row[2]:
                    entries.append(Mapping(
                        title=row[2],
                        language='es',
                        rank=i))
                if row[3]:
                    entries.append(Mapping(
                        title=row[3],
                        language='fr',
                        rank=i))
                if row[4]:
                    entries.append(Mapping(
                        title=row[4],
                        language='ja',
                        rank=i))
                if row[5]:
                    entries.append(Mapping(
                        title=row[5],
                        language='ru',
                        rank=i))

                Mapping.objects.bulk_create(entries)

            # pre-fill questions
            mappings = Mapping.objects.all()
            for mapping in mappings:
                user_inputs = []
                for lang in LANGUAGE_CHOICES:
                    user_inputs.append(UserInput(
                        source=mapping,
                        destination_language=lang[0]
                    ))
                UserInput.objects.bulk_create(user_inputs)

            self.stdout.write('Import done.')

from django.core.management.base import BaseCommand, CommandError
from sectionalignment.models import Mapping, LANGUAGE_CHOICES
import json


class Command(BaseCommand):
    help = 'Imports model generated data into database'

    def add_arguments(self, parser):
        parser.add_argument('tsv_filename', nargs=1, type=str)

    def handle(self, *args, **options):
        # TODO: update when data is line by line
        with open(options['tsv_filename'][0], 'r', encoding='utf-8') as infile:
            for i, row in enumerate(infile):
                row = [x.strip() for x in row]
                entries = []
                if row[0]:
                    entries.append(Mapping(
                        source_title=row[0],
                        source_language='ar',
                        section_rank=i))
                if row[1]:
                    entries.append(Mapping(
                        source_title=row[1],
                        source_language='en',
                        section_rank=i))
                if row[2]:
                    entries.append(Mapping(
                        source_title=row[2],
                        source_language='es',
                        section_rank=i))
                if row[3]:
                    entries.append(Mapping(
                        source_title=row[3],
                        source_language='fr',
                        section_rank=i))
                if row[4]:
                    entries.append(Mapping(
                        source_title=row[4],
                        source_language='ja',
                        section_rank=i))
                if row[5]:
                    entries.append(Mapping(
                        source_title=row[5],
                        source_language='ru',
                        section_rank=i))

                Mapping.objects.bulk_create(entries)
            self.stdout.write('Import done.')

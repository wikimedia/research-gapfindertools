# from django.core.management.base import BaseCommand, CommandError
# from sectionmapping.models import Section
# import json


# class Command(BaseCommand):
#     help = 'Imports model generated data into database'

#     def add_arguments(self, parser):
#         parser.add_argument('json_filename', nargs=1, type=str)
#         parser.add_argument('language', nargs=1, type=str)

#     def handle(self, *args, **options):
#         # TODO: update when data is line by line
#         with open(options['json_filename']) as json_file:
#             json_data = json.loads(json_file)
#             for title, data in json_data.values():
#                 section = Section(title=title, language=options['language'],
#                                   rank=data['rank'], targets=json.dumps(

#         for poll_id in options['json_filename']:
#             try:
#                 poll = Poll.objects.get(pk=poll_id)
#             except Poll.DoesNotExist:
#                 raise CommandError('Poll "%s" does not exist' % poll_id)

#             poll.opened = False
#             poll.save()

#             self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))

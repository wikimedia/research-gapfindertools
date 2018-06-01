from django.core.management.base import BaseCommand

from sectionalignment.models import UserInput, LANGUAGE_CHOICES


class Command(BaseCommand):
    help = 'Prints stats on each language pair.'

    def handle(self, *args, **options):
        stats = {}
        for s, _ in LANGUAGE_CHOICES:
            for d, _ in LANGUAGE_CHOICES:
                if s == d:
                    continue
                user_inputs = UserInput.objects.filter(
                    source__language=s,
                    destination_language=d
                )
                stats['%s-%s' % (s, d)] = (
                    user_inputs.filter(done=True).count(),
                    user_inputs.filter(done=False).count()
                )
        stats_l = list(stats.items())
        stats_l.sort(key=lambda x: x[0])

        print('|%s|%s|%s|' % (
            'language pair'.ljust(13),
            'done'.ljust(4),
            'not done'.ljust(8)
        ))
        for pair in stats_l:
            print('|%s|%s|%s|' % (
                pair[0].ljust(13),
                str(pair[1][0]).ljust(4),
                str(pair[1][1]).ljust(8)
            ))

import csv
from io import StringIO


from django.contrib import admin
from django.http import HttpResponse

from .models import Mapping, UserInput

admin.site.register(Mapping)


class UserInputAdmin(admin.ModelAdmin):
    actions = ['download_tsv']
    list_filter = ['done', 'user_session_key']
    search_fields = ['source__title']

    def download_tsv(self, request, queryset):
        f = StringIO()
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(["source_lang", "source_title", "destination_language",
                         "destination_title", "user_session_key"])
        for row in queryset:
            writer.writerow([row.source.language, row.source.title,
                             row.destination_language, row.destination_title,
                             row.user_session_key])
        f.seek(0)
        response = HttpResponse(f, content_type='text/tsv')
        response['Content-Disposition'] = 'attachment; filename=user_input.tsv'
        return response
    download_tsv.short_description = "Download selected user inputs"


admin.site.register(UserInput, UserInputAdmin)

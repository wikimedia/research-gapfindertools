from django.contrib import admin

from .models import Mapping, UserInput

admin.site.register(Mapping)


class UserInputAdmin(admin.ModelAdmin):
    search_fields = ['source__title']
    list_filter = ['user_session_key']


admin.site.register(UserInput, UserInputAdmin)

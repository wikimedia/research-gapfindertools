from django.contrib import admin

from .models import Mapping, UserInput

admin.site.register(Mapping)


class UserInputAdmin(admin.ModelAdmin):
    search_fields = ['source__title']


admin.site.register(UserInput, UserInputAdmin)

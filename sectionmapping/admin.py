from django.contrib import admin

from .models import Mapper, Mapping, Section, MappingSummary

admin.site.register(Mapper)
admin.site.register(Mapping)
admin.site.register(Section)
admin.site.register(MappingSummary)

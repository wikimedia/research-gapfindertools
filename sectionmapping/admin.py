from django.contrib import admin

from .models import Mapper, MapperSectionMapping, Section, SectionMapping

admin.site.register(Mapper)
admin.site.register(MapperSectionMapping)
admin.site.register(Section)
admin.site.register(SectionMapping)

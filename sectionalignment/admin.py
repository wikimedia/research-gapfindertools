from django.contrib import admin

from .models import ModelMapping, User, UserMapping, UserMappingSummary

admin.site.register(ModelMapping)
admin.site.register(User)
admin.site.register(UserMapping)
admin.site.register(UserMappingSummary)

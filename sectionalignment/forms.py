from django import forms
from . import models


class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['wiki_username', 'ar_proficiency', 'en_proficiency',
                  'es_proficiency', 'fr_proficiency', 'ja_proficiency',
                  'ru_proficiency']

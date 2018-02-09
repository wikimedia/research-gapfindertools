from django.forms import ModelForm
from . import models


class TranslatorForm(ModelForm):
    class Meta:
        model = models.Translator
        fields = ['username', 'ar_proficiency', 'en_proficiency',
                  'es_proficiency', 'fr_proficiency', 'ja_proficiency',
                  'ru_proficiency']

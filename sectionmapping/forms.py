from django.forms import ModelForm
from . import models


class MapperForm(ModelForm):
    class Meta:
        model = models.Mapper
        fields = ['wiki_username', 'ar_proficiency', 'en_proficiency',
                  'es_proficiency', 'fr_proficiency', 'ja_proficiency',
                  'ru_proficiency']

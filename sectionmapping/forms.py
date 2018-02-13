from django import forms
from . import models


class MapperForm(forms.ModelForm):
    class Meta:
        model = models.Mapper
        fields = ['wiki_username', 'ar_proficiency', 'en_proficiency',
                  'es_proficiency', 'fr_proficiency', 'ja_proficiency',
                  'ru_proficiency']


class MapForm(forms.Form):
    lang = forms.HiddenInput()
    title = forms.HiddenInput()
    ar = forms.Select()
    en = forms.Select()
    es = forms.Select()
    fr = forms.Select()
    ja = forms.Select()
    ru = forms.Select()

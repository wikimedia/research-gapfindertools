from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

import json


LANGUAGE_CHOICES = (
    ('ar', 'Arabic'),
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('ja', 'Japanese'),
    ('ru', 'Russian')
)

MIN_PROFICIENCY = '3'  # minimum proficiency needed for mapping

LANGUAGE_PROFICIENCIES = (
    ('0', "0 - If you don't understand the language at all."),
    ('1', "1 - Basic ability - enough to understand written "
     "material or simple questions in this language."),
    ('2', "2 - Intermediate ability - enough for editing or discussions."),
    ('3', "3 - Advanced level - though you can write in this "
     "language with no problem, some small errors might occur."),
    ('4', "4 - Near-native level—although it's not your first language "
     "from birth, your ability is something like that of a native speaker."),
    ('5', "5 - Professional proficiency."),
    ('N', "N - Native speakers who use a language every day and have a "
     "thorough grasp of it, including colloquialisms and idioms.")
)


class Mapper(models.Model):
    """User info"""
    wiki_username = models.CharField("Wiki username", max_length=255)
    ar_proficiency = models.CharField(
        blank=True, max_length=1, choices=LANGUAGE_PROFICIENCIES)
    en_proficiency = models.CharField(
        blank=True, max_length=1, choices=LANGUAGE_PROFICIENCIES)
    es_proficiency = models.CharField(
        blank=True, max_length=1, choices=LANGUAGE_PROFICIENCIES)
    fr_proficiency = models.CharField(
        blank=True, max_length=1, choices=LANGUAGE_PROFICIENCIES)
    ja_proficiency = models.CharField(
        blank=True, max_length=1, choices=LANGUAGE_PROFICIENCIES)
    ru_proficiency = models.CharField(
        blank=True, max_length=1, choices=LANGUAGE_PROFICIENCIES)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.wiki_username

    def get_source_language(self):
        source_language = None
        source_proficiency = MIN_PROFICIENCY
        if self.ar_proficiency >= source_proficiency:
            source_proficiency = self.ar_proficiency
            source_language = 'ar'
        if self.en_proficiency >= source_proficiency:
            source_proficiency = self.en_proficiency
            source_language = 'en'
        if self.es_proficiency >= source_proficiency:
            source_proficiency = self.es_proficiency
            source_language = 'es'
        if self.fr_proficiency >= source_proficiency:
            source_proficiency = self.fr_proficiency
            source_language = 'fr'
        if self.ja_proficiency >= source_proficiency:
            source_proficiency = self.ja_proficiency
            source_language = 'ja'
        if self.ru_proficiency >= source_proficiency:
            source_proficiency = self.ru_proficiency
            source_language = 'ru'
        return source_language

    def get_target_languages(self):
        all_languages = set()
        if self.ar_proficiency >= MIN_PROFICIENCY:
            all_languages.add('ar')
        if self.en_proficiency >= MIN_PROFICIENCY:
            all_languages.add('en')
        if self.es_proficiency >= MIN_PROFICIENCY:
            all_languages.add('es')
        if self.fr_proficiency >= MIN_PROFICIENCY:
            all_languages.add('fr')
        if self.ja_proficiency >= MIN_PROFICIENCY:
            all_languages.add('ja')
        if self.ru_proficiency >= MIN_PROFICIENCY:
            all_languages.add('ru')

        source_language = self.get_source_language()
        if source_language in all_languages:
            all_languages.remove(source_language)
        return list(all_languages)


class Section(models.Model):
    """Model generated mappings"""
    title = models.TextField()
    language = models.CharField(choices=LANGUAGE_CHOICES,
                                db_index=True, max_length=8)
    # lower rank = section appears more frequently
    rank = models.PositiveIntegerField(db_index=True)
    targets = models.TextField(
        "JSON dump of section targets in multiple languages.")

    class Meta:
        unique_together = ('title', 'language')

    def __str__(self):
        return "%s: %s" % (self.language, self.title)


class Mapping(models.Model):
    """User generated mappings"""
    mapper = models.ForeignKey(Mapper, on_delete=models.CASCADE)
    source = models.ForeignKey(Section, on_delete=models.CASCADE)
    targets = models.TextField("JSON dump of section targets. "
                               "Includes user defined targets.")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('mapper', 'source')

    def __str__(self):
        return "%s: %s" % (self.mapper, self.source)


class MappingSummary(models.Model):
    """Used to query missing mappings"""
    source = models.ForeignKey(Section, on_delete=models.CASCADE)
    ar_count = models.PositiveSmallIntegerField(default=0)
    en_count = models.PositiveSmallIntegerField(default=0)
    es_count = models.PositiveSmallIntegerField(default=0)
    fr_count = models.PositiveSmallIntegerField(default=0)
    ja_count = models.PositiveSmallIntegerField(default=0)
    ru_count = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['source__rank', 'ar_count', 'en_count',
                    'es_count', 'fr_count', 'ja_count', 'ru_count']

    def __str__(self):
        return str(self.source)


@receiver(post_save, sender=Section)
def create_mapping_summary(sender, instance, **kwargs):
    """Create mapping summary when a new section is created."""
    if kwargs['created']:
        new_mapping_summary = MappingSummary(source=instance)
        new_mapping_summary.save()


@receiver(post_save, sender=Mapping)
def update_mapping_summary(sender, instance, **kwargs):
    """Update mapping summary when a new mapping is created."""
    if kwargs['created']:
        mapping_summary = MappingSummary.objects.get(source=instance.source)
        targets = json.loads(instance.targets)
        if 'ar' in targets:
            mapping_summary.ar_count += 1
        if 'en' in targets:
            mapping_summary.en_count += 1
        if 'es' in targets:
            mapping_summary.es_count += 1
        if 'fr' in targets:
            mapping_summary.fr_count += 1
        if 'ja' in targets:
            mapping_summary.ja_count += 1
        if 'ru' in targets:
            mapping_summary.ru_count += 1
        mapping_summary.save()

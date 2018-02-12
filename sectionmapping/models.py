from django.db import models


LANGUAGE_CHOICES = (
    ('ar', 'Arabic'),
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('ja', 'Japanese'),
    ('ru', 'Russian')
)

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


class Section(models.Model):
    title = models.TextField("Section title")
    language = models.CharField(
        "Section language",
        choices=LANGUAGE_CHOICES,
        max_length=8
    )
    source_rank = models.PositiveIntegerField(
        "Section rank in source language",
        db_index=True)

    class Meta:
        unique_together = ('title', 'language')

    def __str__(self):
        return "%s: %s" % (self.language, self.title)


class SectionMapping(models.Model):
    source = models.ForeignKey(Section, on_delete=models.CASCADE,
                               related_name="source")
    target = models.ForeignKey(Section, on_delete=models.CASCADE,
                               related_name="target")
    target_rank = models.PositiveIntegerField(
        "Section rank in target language")

    class Meta:
        unique_together = ('source', 'target')

    def __str__(self):
        return "%s–%s: %s — %s" % (self.source.language, self.target.language,
                                   self.source.title, self.target.title)


class MapperSectionMapping(models.Model):
    mapper = models.ForeignKey(Mapper, on_delete=models.CASCADE)
    section_mapping = models.ForeignKey(SectionMapping,
                                        on_delete=models.CASCADE)

    class Meta:
        unique_together = ('mapper', 'section_mapping')

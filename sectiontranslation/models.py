from django.db import models

SECTION_LANGUAGE_CHOICES = (
    ('ar', 'Arabic'),
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('ja', 'Japanese'),
    ('ru', 'Russian')
)

TRANSLATOR_LANGUAGE_PROFICIENCIES = (
    ('0', "If you don't understand the language at all."),
    ('1', "Basic ability - enough to understand written "
     "material or simple questions in this language."),
    ('2', "Intermediate ability - enough for editing or discussions."),
    ('3', "Advanced level - though you can write in this "
     "language with no problem, some small errors might occur."),
    ('4', "Near-native level—although it's not your first language "
     "from birth, your ability is something like that of a native speaker."),
    ('5', "Professional proficiency."),
    ('N', "Native speakers who use a language every day and have a thorough "
     "grasp of it, including colloquialisms and idioms.")
)


class Section(models.Model):
    title = models.TextField()
    language = models.CharField(
        db_index=True, choices=SECTION_LANGUAGE_CHOICES, max_length=8)
    ranking = models.PositiveIntegerField(db_index=True)
    # JSON dump of title's translations
    translation = models.TextField()

    class Meta:
        unique_together = ('title', 'language')

    def __str__(self):
        return "%s: %s" % (self.language, self.title)


class Translator(models.Model):
    # TODO add 'created'
    username = models.CharField(max_length=255)
    ar_proficiency = models.CharField(
        max_length=1, choices=TRANSLATOR_LANGUAGE_PROFICIENCIES)
    en_proficiency = models.CharField(
        max_length=1, choices=TRANSLATOR_LANGUAGE_PROFICIENCIES)
    es_proficiency = models.CharField(
        max_length=1, choices=TRANSLATOR_LANGUAGE_PROFICIENCIES)
    fr_proficiency = models.CharField(
        max_length=1, choices=TRANSLATOR_LANGUAGE_PROFICIENCIES)
    ja_proficiency = models.CharField(
        max_length=1, choices=TRANSLATOR_LANGUAGE_PROFICIENCIES)
    ru_proficiency = models.CharField(
        max_length=1, choices=TRANSLATOR_LANGUAGE_PROFICIENCIES)

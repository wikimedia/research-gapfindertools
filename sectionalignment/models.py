from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# import json


LANGUAGE_CHOICES = (
    ('ar', 'Arabic'),
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('ja', 'Japanese'),
    ('ru', 'Russian')
)


class Mapping(models.Model):
    "Mappings and user inputs"
    title = models.TextField()
    language = models.CharField(
        choices=LANGUAGE_CHOICES, db_index=True, max_length=2
    )
    # lower section_rank = section appears more frequently
    rank = models.PositiveIntegerField(db_index=True)

    def __str__(self):
        return "%s: %s" % (self.language, self.title)


class UserInput(models.Model):
    source = models.ForeignKey(Mapping, on_delete=models.CASCADE)
    destination_language = models.CharField(
        choices=LANGUAGE_CHOICES, db_index=True, max_length=2
    )
    # Contains the list of user's input values.
    destination_title = models.TextField()
    # Has the user filled out this mapping?
    done = models.BooleanField(db_index=True, default=False)
    # When did the user see the question?
    # If this time is more than 5 mins old, then we can show this
    # question to someone else.
    start_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s: %s" % (self.source.language,
                                self.destination_language,
                                self.source.title)

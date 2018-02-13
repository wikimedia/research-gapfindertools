# Generated by Django 2.0.2 on 2018-02-13 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mapper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wiki_username', models.CharField(max_length=255, verbose_name='Wiki username')),
                ('ar_proficiency', models.CharField(blank=True, choices=[('0', "0 - If you don't understand the language at all."), ('1', '1 - Basic ability - enough to understand written material or simple questions in this language.'), ('2', '2 - Intermediate ability - enough for editing or discussions.'), ('3', '3 - Advanced level - though you can write in this language with no problem, some small errors might occur.'), ('4', "4 - Near-native level—although it's not your first language from birth, your ability is something like that of a native speaker."), ('5', '5 - Professional proficiency.'), ('N', 'N - Native speakers who use a language every day and have a thorough grasp of it, including colloquialisms and idioms.')], max_length=1)),
                ('en_proficiency', models.CharField(blank=True, choices=[('0', "0 - If you don't understand the language at all."), ('1', '1 - Basic ability - enough to understand written material or simple questions in this language.'), ('2', '2 - Intermediate ability - enough for editing or discussions.'), ('3', '3 - Advanced level - though you can write in this language with no problem, some small errors might occur.'), ('4', "4 - Near-native level—although it's not your first language from birth, your ability is something like that of a native speaker."), ('5', '5 - Professional proficiency.'), ('N', 'N - Native speakers who use a language every day and have a thorough grasp of it, including colloquialisms and idioms.')], max_length=1)),
                ('es_proficiency', models.CharField(blank=True, choices=[('0', "0 - If you don't understand the language at all."), ('1', '1 - Basic ability - enough to understand written material or simple questions in this language.'), ('2', '2 - Intermediate ability - enough for editing or discussions.'), ('3', '3 - Advanced level - though you can write in this language with no problem, some small errors might occur.'), ('4', "4 - Near-native level—although it's not your first language from birth, your ability is something like that of a native speaker."), ('5', '5 - Professional proficiency.'), ('N', 'N - Native speakers who use a language every day and have a thorough grasp of it, including colloquialisms and idioms.')], max_length=1)),
                ('fr_proficiency', models.CharField(blank=True, choices=[('0', "0 - If you don't understand the language at all."), ('1', '1 - Basic ability - enough to understand written material or simple questions in this language.'), ('2', '2 - Intermediate ability - enough for editing or discussions.'), ('3', '3 - Advanced level - though you can write in this language with no problem, some small errors might occur.'), ('4', "4 - Near-native level—although it's not your first language from birth, your ability is something like that of a native speaker."), ('5', '5 - Professional proficiency.'), ('N', 'N - Native speakers who use a language every day and have a thorough grasp of it, including colloquialisms and idioms.')], max_length=1)),
                ('ja_proficiency', models.CharField(blank=True, choices=[('0', "0 - If you don't understand the language at all."), ('1', '1 - Basic ability - enough to understand written material or simple questions in this language.'), ('2', '2 - Intermediate ability - enough for editing or discussions.'), ('3', '3 - Advanced level - though you can write in this language with no problem, some small errors might occur.'), ('4', "4 - Near-native level—although it's not your first language from birth, your ability is something like that of a native speaker."), ('5', '5 - Professional proficiency.'), ('N', 'N - Native speakers who use a language every day and have a thorough grasp of it, including colloquialisms and idioms.')], max_length=1)),
                ('ru_proficiency', models.CharField(blank=True, choices=[('0', "0 - If you don't understand the language at all."), ('1', '1 - Basic ability - enough to understand written material or simple questions in this language.'), ('2', '2 - Intermediate ability - enough for editing or discussions.'), ('3', '3 - Advanced level - though you can write in this language with no problem, some small errors might occur.'), ('4', "4 - Near-native level—although it's not your first language from birth, your ability is something like that of a native speaker."), ('5', '5 - Professional proficiency.'), ('N', 'N - Native speakers who use a language every day and have a thorough grasp of it, including colloquialisms and idioms.')], max_length=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('targets', models.TextField(verbose_name='JSON dump of section targets. Includes user defined targets.')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('mapper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sectionmapping.Mapper')),
            ],
        ),
        migrations.CreateModel(
            name='MappingSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ar_count', models.PositiveSmallIntegerField(default=0)),
                ('en_count', models.PositiveSmallIntegerField(default=0)),
                ('es_count', models.PositiveSmallIntegerField(default=0)),
                ('fr_count', models.PositiveSmallIntegerField(default=0)),
                ('ja_count', models.PositiveSmallIntegerField(default=0)),
                ('ru_count', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'ordering': ['ar_count', 'en_count', 'es_count', 'fr_count', 'ja_count', 'ru_count'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('language', models.CharField(choices=[('ar', 'Arabic'), ('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), ('ja', 'Japanese'), ('ru', 'Russian')], db_index=True, max_length=8)),
                ('rank', models.PositiveIntegerField(db_index=True)),
                ('targets', models.TextField(verbose_name='JSON dump of section targets in multiple languages.')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='section',
            unique_together={('title', 'language')},
        ),
        migrations.AddField(
            model_name='mappingsummary',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sectionmapping.Section'),
        ),
        migrations.AddField(
            model_name='mapping',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sectionmapping.Section'),
        ),
        migrations.AlterUniqueTogether(
            name='mapping',
            unique_together={('mapper', 'source')},
        ),
    ]

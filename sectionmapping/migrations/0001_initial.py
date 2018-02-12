# Generated by Django 2.0.2 on 2018-02-12 21:18

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
            name='MapperSectionMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mapper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sectionmapping.Mapper')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='Section title')),
                ('language', models.CharField(choices=[('ar', 'Arabic'), ('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), ('ja', 'Japanese'), ('ru', 'Russian')], max_length=8, verbose_name='Section language')),
            ],
        ),
        migrations.CreateModel(
            name='SectionMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_rank', models.PositiveIntegerField(db_index=True, verbose_name='Section rank in source language')),
                ('target_rank', models.PositiveIntegerField(verbose_name='Section rank in target language')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='sectionmapping.Section')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target', to='sectionmapping.Section')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='section',
            unique_together={('title', 'language')},
        ),
        migrations.AddField(
            model_name='mappersectionmapping',
            name='section_mapping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sectionmapping.SectionMapping'),
        ),
        migrations.AlterUniqueTogether(
            name='sectionmapping',
            unique_together={('source', 'target')},
        ),
        migrations.AlterUniqueTogether(
            name='mappersectionmapping',
            unique_together={('mapper', 'section_mapping')},
        ),
    ]

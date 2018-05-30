# Generated by Django 2.0.2 on 2018-05-30 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('language', models.CharField(choices=[('ar', 'Arabic'), ('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), ('ja', 'Japanese'), ('ru', 'Russian')], db_index=True, max_length=2)),
                ('rank', models.PositiveIntegerField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserInput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination_language', models.CharField(choices=[('ar', 'Arabic'), ('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), ('ja', 'Japanese'), ('ru', 'Russian')], db_index=True, max_length=2)),
                ('destination_title', models.TextField()),
                ('done', models.BooleanField(db_index=True, default=False)),
                ('start_time', models.DateTimeField()),
                ('user_session_key', models.CharField(default='', max_length=64)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sectionalignment.Mapping')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='mapping',
            unique_together={('title', 'language')},
        ),
        migrations.AlterUniqueTogether(
            name='userinput',
            unique_together={('source', 'destination_language')},
        ),
    ]

# Generated by Django 3.0.5 on 2020-11-25 19:38

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eduvateApp', '0018_auto_20200825_1643'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonFeedbackCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eduvateApp.Lesson')),
            ],
        ),
    ]
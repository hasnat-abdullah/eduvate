# Generated by Django 3.0.5 on 2020-08-14 16:17

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseApp', '0002_auto_20200810_2345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='what_u_will_learn',
        ),
        migrations.AlterField(
            model_name='course',
            name='course_hours',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='course',
            name='long_description',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='course',
            name='short_description',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='learningpath',
            name='long_description',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='learningpath',
            name='short_description',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]

# Generated by Django 3.0.5 on 2020-06-11 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instructorApp', '0003_user_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructor',
            name='mobile',
        ),
    ]

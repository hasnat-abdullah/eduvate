# Generated by Django 3.0.5 on 2020-08-16 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courseApp', '0005_auto_20200817_0034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='instructor',
        ),
    ]

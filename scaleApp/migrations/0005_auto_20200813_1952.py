# Generated by Django 3.0.5 on 2020-08-13 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scaleApp', '0004_scoringdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scoringdetails',
            name='result',
            field=models.CharField(default='Minimal', max_length=40),
        ),
    ]
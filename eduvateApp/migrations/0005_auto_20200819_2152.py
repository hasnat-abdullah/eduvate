# Generated by Django 3.0.5 on 2020-08-19 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eduvateApp', '0004_auto_20200819_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
    ]

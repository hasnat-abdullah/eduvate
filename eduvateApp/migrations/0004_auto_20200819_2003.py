# Generated by Django 3.0.5 on 2020-08-19 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eduvateApp', '0003_auto_20200819_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video',
            field=models.CharField(max_length=350, null=True),
        ),
    ]

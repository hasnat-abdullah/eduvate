# Generated by Django 3.0.5 on 2020-08-10 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scaleApp', '0001_initial'),
        ('courseApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeasuringScaleForModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='coursemodule',
            name='how_many_time_weekly_accessable',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.DeleteModel(
            name='AnalyzeLevelMeter',
        ),
        migrations.AddField(
            model_name='measuringscaleformodule',
            name='module_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courseApp.CourseModule'),
        ),
        migrations.AddField(
            model_name='measuringscaleformodule',
            name='scale_name',
            field=models.ManyToManyField(to='scaleApp.MeasuringScale'),
        ),
    ]

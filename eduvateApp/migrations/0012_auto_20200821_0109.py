# Generated by Django 3.0.5 on 2020-08-20 19:09

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eduvateApp', '0011_enrolledcourse_updated_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True),
        ),
        migrations.CreateModel(
            name='LessonScale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
                ('lesson_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='eduvateApp.Lesson')),
                ('scale_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eduvateApp.MeasuringScale')),
            ],
        ),
    ]
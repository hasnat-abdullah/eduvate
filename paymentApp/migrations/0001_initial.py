# Generated by Django 3.0.5 on 2020-08-09 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courseApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('bkash', 'BKASH'), ('rocket', 'ROCKET')], default='bkash', max_length=6)),
                ('paid_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('txn_id', models.CharField(max_length=20)),
                ('reference', models.CharField(max_length=100)),
                ('payment_status', models.CharField(choices=[('completed', 'COMPLETED'), ('partial', 'PARTIAL'), ('cancel', 'CANCEL'), ('hold', 'HOLD'), ('pending', 'pending'), ('incomplete', 'INCOMPLETE'), ('refund', 'REFUND')], default='incomplete', max_length=10)),
                ('paid_for_module', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='courseApp.CourseModule')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 3.2.12 on 2023-04-21 16:59

from django.db import migrations, models
import rents.models


class Migration(migrations.Migration):

    dependencies = [
        ('rents', '0004_rent_warning_sent_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='expired_at',
            field=models.DateTimeField(default=rents.models.one_month_from_today, verbose_name='Окончание аренды'),
        ),
    ]
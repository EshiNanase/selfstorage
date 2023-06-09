# Generated by Django 3.2.12 on 2023-04-19 11:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('storage', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('box_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость аренды в сутки')),
                ('status', models.CharField(choices=[('ACTIVE', 'Активна'), ('CLOSED', 'Завершена'), ('EXPIRED', 'Просрочена')], max_length=20, verbose_name='Статус')),
                ('started_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Начало аренды')),
                ('expired_at', models.DateTimeField(verbose_name='Окончание аренды')),
                ('closed_at', models.DateTimeField(verbose_name='Завершена')),
                ('box', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rents', to='storage.box', verbose_name='Бокс')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rents', to=settings.AUTH_USER_MODEL, verbose_name='Арендатор')),
            ],
            options={
                'verbose_name': 'Аренда',
                'verbose_name_plural': 'Аренды',
            },
        ),
    ]

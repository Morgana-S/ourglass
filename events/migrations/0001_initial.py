# Generated by Django 5.2.1 on 2025-05-27 12:58

import cloudinary.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=75)),
                ('event_date', models.DateTimeField()),
                ('is_online', models.BooleanField()),
                ('url_or_address', models.CharField(max_length=100)),
                ('maximum_attendees', models.PositiveSmallIntegerField()),
                ('short_description', models.TextField(max_length=200)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('long_description', models.TextField(max_length=3000)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('event_organiser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tickets', models.PositiveSmallIntegerField(choices=[(1, 'x1'), (2, 'x2'), (3, 'x3'), (4, 'x4')])),
                ('ticketholder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticketholder', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='events.event')),
            ],
        ),
    ]

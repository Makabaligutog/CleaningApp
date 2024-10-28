# Generated by Django 5.0.4 on 2024-10-28 04:23

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('photo', models.ImageField(upload_to='service_photos/')),
                ('rating', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cleaning_service', models.CharField(choices=[('residential', 'Residential Cleaning'), ('commercial', 'Commercial Cleaning'), ('deep-cleaning', 'Deep Cleaning'), ('move-in-out', 'Move-in/Move-out Cleaning'), ('carpet-cleaning', 'Carpet Cleaning'), ('upholstery-cleaning', 'Upholstery Cleaning'), ('window-cleaning', 'Window Cleaning'), ('eco-friendly', 'Eco-friendly Green Cleaning')], max_length=20)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(default='Unknown', max_length=100)),
                ('contact_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('additional_info', models.TextField(blank=True, null=True)),
                ('status', models.CharField(default='Confirmed', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 4.2.13 on 2024-09-05 00:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0017_remove_meal_health_status_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HealthStatus',
        ),
    ]

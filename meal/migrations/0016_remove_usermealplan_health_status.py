# Generated by Django 4.2.13 on 2024-09-05 00:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0015_alter_meal_options_usermealplan_health_status_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermealplan',
            name='health_status',
        ),
    ]

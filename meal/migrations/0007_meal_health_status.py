# Generated by Django 4.2.13 on 2024-08-26 04:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0006_remove_daymealplan_afternoon_snack_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='health_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meals', to='meal.healthstatus'),
        ),
    ]

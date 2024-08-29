# Generated by Django 4.2.13 on 2024-08-26 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0008_alter_mealplan_days_usermealplan_daymealcompletion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermealplan',
            name='height',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Height (cm)'),
        ),
        migrations.AlterField(
            model_name='usermealplan',
            name='start_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='usermealplan',
            name='weight',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Weight (kg)'),
        ),
    ]
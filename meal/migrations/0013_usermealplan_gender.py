# Generated by Django 4.2.13 on 2024-08-28 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0012_remove_usermealplan_age_usermealplan_birthdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermealplan',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=10),
        ),
    ]

# Generated by Django 4.2.13 on 2024-08-28 02:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0011_alter_daymealcompletion_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermealplan',
            name='age',
        ),
        migrations.AddField(
            model_name='usermealplan',
            name='birthdate',
            field=models.DateField(default=datetime.datetime(2024, 8, 28, 2, 36, 13, 101796, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
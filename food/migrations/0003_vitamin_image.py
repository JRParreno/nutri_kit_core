# Generated by Django 4.2.13 on 2024-07-15 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_vitamin_food_vitamins'),
    ]

    operations = [
        migrations.AddField(
            model_name='vitamin',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/vitamins/'),
        ),
    ]

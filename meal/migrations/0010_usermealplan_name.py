# Generated by Django 4.2.13 on 2024-08-26 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0009_alter_usermealplan_height_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermealplan',
            name='name',
            field=models.CharField(default='Juan Dela Cruz', max_length=150, verbose_name='Child full name'),
            preserve_default=False,
        ),
    ]

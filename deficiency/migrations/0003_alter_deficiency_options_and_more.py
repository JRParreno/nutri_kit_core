# Generated by Django 4.2.13 on 2024-07-06 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deficiency', '0002_deficiency_deficiencysymptom_deficiency_symptoms'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deficiency',
            options={'verbose_name': 'Deficiency', 'verbose_name_plural': 'Deficiencies'},
        ),
        migrations.AlterUniqueTogether(
            name='deficiencysymptom',
            unique_together={('deficiency', 'symptom')},
        ),
    ]

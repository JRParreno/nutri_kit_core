# Generated by Django 4.2.13 on 2024-07-05 23:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deficiency', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deficiency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DeficiencySymptom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deficiency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deficiency.deficiency')),
                ('symptom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deficiency.symptom')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='deficiency',
            name='symptoms',
            field=models.ManyToManyField(through='deficiency.DeficiencySymptom', to='deficiency.symptom'),
        ),
    ]

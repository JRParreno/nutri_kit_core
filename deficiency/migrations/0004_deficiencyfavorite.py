# Generated by Django 4.2.13 on 2024-09-05 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_remove_userprofile_address'),
        ('deficiency', '0003_alter_deficiency_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeficiencyFavorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deficiency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deficiency.deficiency')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.userprofile')),
            ],
            options={
                'unique_together': {('deficiency', 'user_profile')},
            },
        ),
    ]
# Generated by Django 4.2.13 on 2024-07-12 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trivia', '0002_remove_question_correct_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_banner',
            field=models.ImageField(blank=True, null=True, upload_to='images/question/'),
        ),
    ]

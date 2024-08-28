# Generated by Django 4.2.13 on 2024-08-26 23:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meal', '0007_meal_health_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mealplan',
            name='days',
            field=models.IntegerField(default=7),
        ),
        migrations.CreateModel(
            name='UserMealPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('age', models.IntegerField()),
                ('height', models.DecimalField(decimal_places=2, max_digits=5)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('health_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meal.healthstatus')),
                ('meal_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_meal_plans', to='meal.mealplan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_meal_plans', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DayMealCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('day_meal_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='day_meal_completions', to='meal.daymealplan')),
                ('user_meal_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='day_meal_completions', to='meal.usermealplan')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

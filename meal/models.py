from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from core.base_models import BaseModel

"""
    underweight or overweight or obese: formula 3
    stunted: formula 2
    wasted: formula 1
"""

STATUS_CHOICES = [
    ('underweight', 'Underweight'),
    ('wasted', 'Wasted'),
    ('overweight', 'Overweight'),
    ('obese', 'Obese'),
    ('stunted', 'Stunted'),
]

class Meal(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    calories = models.IntegerField()
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    carbs = models.DecimalField(max_digits=5, decimal_places=2)
    fats = models.DecimalField(max_digits=5, decimal_places=2)
    health_status_info = models.CharField(max_length=20, choices=STATUS_CHOICES, default='wasted')


    class Meta:
        ordering = ['name',]
        
    def __str__(self):
        return self.name

class MealPlan(BaseModel):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    health_status_info = models.CharField(max_length=20, choices=STATUS_CHOICES, default='wasted')
    days = models.IntegerField(default=7)  # Number of days the meal plan covers

    def __str__(self):
        return f"{self.name} - {self.health_status_info} ({self.days} days)"


class DayMealPlan(BaseModel):
    meal_plan = models.ForeignKey(MealPlan, related_name='day_meals', on_delete=models.CASCADE)
    day_number = models.IntegerField()  # Day number within the meal plan
    breakfast = models.ForeignKey(Meal, related_name='breakfast_meals', on_delete=models.CASCADE, blank=True, null=True)
    mid_morning_snack = models.ForeignKey(Meal, related_name='mid_morning_snacks', on_delete=models.CASCADE, blank=True, null=True)
    lunch = models.ForeignKey(Meal, related_name='lunch_meals', on_delete=models.CASCADE, blank=True, null=True)
    afternoon_snack = models.ForeignKey(Meal, related_name='afternoon_snacks', on_delete=models.CASCADE, blank=True, null=True)
    dinner = models.ForeignKey(Meal, related_name='dinner_meals', on_delete=models.CASCADE, blank=True, null=True)
    evening_snack = models.ForeignKey(Meal, related_name='evening_snacks', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        unique_together = ('meal_plan', 'day_number')

    def __str__(self):
        return f"Day {self.day_number} of {self.meal_plan}"


class UserMealPlan(BaseModel):
    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    
    MALE = 'M'
    FEMALE = 'F'

    
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_meal_plans')
    name = models.CharField(verbose_name='Child full name', max_length=150)
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='user_meal_plans')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)
    birthdate = models.DateField()
    height = models.DecimalField(verbose_name='Height (cm)', max_digits=5, decimal_places=2)  # height in cm
    weight = models.DecimalField(verbose_name='Weight (kg)', max_digits=5, decimal_places=2)  # weight in kg
    health_status_info = models.CharField(max_length=20, choices=STATUS_CHOICES, default='wasted')
    gender = models.CharField(choices=GENDER_CHOICES, default=MALE, max_length=10)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.day_meal_completions.exists():
            day_meal_plans = DayMealPlan.objects.filter(meal_plan=self.meal_plan).order_by('day_number')
            for day_meal_plan in day_meal_plans:
                completion_date = self.start_date + timedelta(days=day_meal_plan.day_number - 1)
                DayMealCompletion.objects.create(user_meal_plan=self, day_meal_plan=day_meal_plan, date=completion_date)


    def __str__(self):
        return f"{self.user.username} - {self.meal_plan.name} ({self.health_status_info})"
    

class DayMealCompletion(BaseModel):
    user_meal_plan = models.ForeignKey(UserMealPlan, on_delete=models.CASCADE, related_name='day_meal_completions')
    day_meal_plan = models.ForeignKey(DayMealPlan, on_delete=models.CASCADE, related_name='day_meal_completions')
    date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_meal_plan.user.username} - Day {self.day_meal_plan.day_number} of {self.user_meal_plan.meal_plan.name}"
from django.contrib import admin
from .models import DayMealPlan,  Meal, MealPlan, UserMealPlan, DayMealCompletion
from unfold.admin import ModelAdmin



@admin.register(Meal)
class MealAdminView(ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name',]
    list_filter = ['health_status_info',]


@admin.register(MealPlan)
class MealPlanAdminView(ModelAdmin):
    list_display = ['name', 'health_status_info', 'age', 'created_at', 'updated_at']
    search_fields = ['name',]


@admin.register(DayMealPlan)
class DayMealPlanAdminView(ModelAdmin):
    autocomplete_fields = [
        'breakfast',
        'mid_morning_snack',
        'lunch',
        'afternoon_snack',
        'dinner',
        'evening_snack',
    ]
    list_display = ['meal_plan', 'day_number', 'created_at', 'updated_at']
    search_fields = ['meal_plan__name',]


@admin.register(UserMealPlan)
class UserMealPlanAdminView(ModelAdmin):
    list_display = ['user', 'meal_plan', 'health_status_info', 'start_date']
    search_fields = ['meal_plan__name', 'user__first_name', 'user__last_name', ]
    list_filter = ['health_status_info',]

@admin.register(DayMealCompletion)
class DayMealCompletionAdminView(ModelAdmin):
    list_display = ['user_meal_plan', 'day_meal_plan', 'date', 'completed']
    search_fields = ['day_meal_plan__meal_plan__name', 'user_meal_plan__user__first_name', 'user_meal_plan__user__last_name', ]
    list_filter = ['completed',]

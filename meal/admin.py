from django.contrib import admin
from .models import DayMealPlan, HealthStatus, Meal, MealPlan, UserMealPlan, DayMealCompletion
from unfold.admin import ModelAdmin


@admin.register(HealthStatus)
class HealthStatusAdminView(ModelAdmin):
    list_display = ['status', 'created_at', 'updated_at']
    search_fields = ['status',]

@admin.register(Meal)
class MealAdminView(ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name',]
    list_filter = ['health_status',]


@admin.register(MealPlan)
class MealPlanAdminView(ModelAdmin):
    list_display = ['name', 'health_status', 'age', 'created_at', 'updated_at']
    search_fields = ['name',]


class HealthStatusFilter(admin.SimpleListFilter):
    title = 'Health Status'
    parameter_name = 'health_status'

    def lookups(self, request, model_admin):
        # Generate a list of tuples (id, status) from HealthStatus objects
        health_statuses = HealthStatus.objects.all()
        return [(hs.id, hs.status) for hs in health_statuses]

    def queryset(self, request, queryset):
        # Filter DayMealPlan records based on selected HealthStatus
        if self.value():
            return queryset.filter(meal_plan__health_status__id__exact=self.value())
        return queryset

@admin.register(DayMealPlan)
class DayMealPlanAdminView(ModelAdmin):
    list_display = ['meal_plan', 'day_number', 'created_at', 'updated_at']
    search_fields = ['meal_plan__name',]
    list_filter = (HealthStatusFilter,)


@admin.register(UserMealPlan)
class UserMealPlanAdminView(ModelAdmin):
    list_display = ['user', 'meal_plan', 'health_status', 'start_date']
    search_fields = ['meal_plan__name', 'user__first_name', 'user__last_name', ]
    list_filter = ['health_status',]

@admin.register(DayMealCompletion)
class DayMealCompletionAdminView(ModelAdmin):
    list_display = ['user_meal_plan', 'day_meal_plan', 'date', 'completed']
    search_fields = ['day_meal_plan__meal_plan__name', 'user_meal_plan__user__first_name', 'user_meal_plan__user__last_name', ]
    list_filter = ['completed',]

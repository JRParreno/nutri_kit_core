from rest_framework import serializers
from .models import (Meal, HealthStatus, UserMealPlan, 
                     MealPlan, DayMealCompletion, DayMealPlan)


class UserMealPlanRegisterSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=150)
    birthdate = serializers.DateField(format="%m/%d/%Y", input_formats=["%m/%d/%Y"], required=True)
    height = serializers.DecimalField(required=True, max_digits=5, decimal_places=2)
    weight = serializers.DecimalField(required=True, max_digits=5, decimal_places=2)
    health_status = serializers.ChoiceField(choices=HealthStatus.STATUS_CHOICES, required=True)
    gender = serializers.ChoiceField(choices=UserMealPlan.GENDER_CHOICES, required=True)
    class Meta:
        fields = ['name', 'birthdate', 'height', 
                  'weight', 'health_status', 'gender',
                  ]


class HealthStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthStatus
        fields = '__all__'



class UserListMealPlanSerializer(serializers.ModelSerializer):
    health_status = HealthStatusSerializer()

    class Meta:
        model = UserMealPlan
        fields = '__all__'


class UserMealPlanSerializer(serializers.ModelSerializer):
    health_status = HealthStatusSerializer()

    class Meta:
        model = UserMealPlan
        exclude = ['meal_plan',]


class MealSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Meal
        exclude = ['health_status',]

class DayMealPlanSerializer(serializers.ModelSerializer):
    breakfast = MealSerializer()
    mid_morning_snack = MealSerializer()
    lunch = MealSerializer()
    afternoon_snack = MealSerializer()
    dinner = MealSerializer()
    evening_snack = MealSerializer()

    class Meta:
        model = DayMealPlan
        exclude = ['meal_plan',]

class DayMealCompletionSerializer(serializers.ModelSerializer):
    day_meal_plan = DayMealPlanSerializer()
    
    class Meta:
        model = DayMealCompletion
        exclude = ['user_meal_plan', ]

        
class MealPlanSerializer(serializers.ModelSerializer):
    health_status = HealthStatusSerializer()
    day_meal_completion = serializers.SerializerMethodField()
    user_meal_plan = serializers.SerializerMethodField()
    
    class Meta:
        model = MealPlan
        fields = ['name', 'health_status', 'days', 'day_meal_completion', 'user_meal_plan']
    
    def __init__(self, *args, **kwargs):
        # init context and request
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        super(MealPlanSerializer, self).__init__(*args, **kwargs)

    def get_day_meal_completion(self, obj):
        mealplan_id = self.context.get('mealplan_id')
        if not mealplan_id:
            return []

        # Fetch DayMealCompletion records based on the meal_plan_id
        day_meal_completions = DayMealCompletion.objects.filter(user_meal_plan=obj, day_meal_plan__meal_plan__id=mealplan_id)
        return DayMealCompletionSerializer(day_meal_completions, many=True).data

    def get_user_meal_plan(self, obj):
        usermealplan_id = self.context.get('usermealplan_id')
        if not usermealplan_id:
            return {}

        # Fetch DayMealCompletion records based on the meal_plan_id
        user_meal_plan = UserMealPlan.objects.get(pk=usermealplan_id)
        return UserMealPlanSerializer(user_meal_plan).data


    def get_meal_plan(self, obj):
        mealplan_id = self.context.get('mealplan_id')
        try:
            meal_plan = MealPlan.objects.get(pk=mealplan_id)
            return MealPlanSerializer(meal_plan).data
        except MealPlan.DoesNotExist:
            return None
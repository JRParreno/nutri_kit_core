from rest_framework import serializers
from .models import (Meal, UserMealPlan, 
                     MealPlan, DayMealCompletion, DayMealPlan)
from decimal import Decimal


class UserMealPlanRegisterSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=150)
    birthdate = serializers.DateField(format="%m/%d/%Y", input_formats=["%m/%d/%Y"], required=True)
    height = serializers.DecimalField(required=True, max_digits=5, decimal_places=2)
    weight = serializers.DecimalField(required=True, max_digits=5, decimal_places=2)
    gender = serializers.ChoiceField(choices=UserMealPlan.GENDER_CHOICES, required=True)
    class Meta:
        fields = ['name', 'birthdate', 'height', 
                  'weight', 'gender',
                  ]

class UserListMealPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserMealPlan
        fields = '__all__'


class UserMealPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserMealPlan
        fields = '__all__'
        


class MealSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Meal
        fields = '__all__'

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
    day_meal_completion = serializers.SerializerMethodField()
    user_meal_plan = serializers.SerializerMethodField()
    total_calories = serializers.SerializerMethodField()
    total_protein = serializers.SerializerMethodField()
    total_carbs = serializers.SerializerMethodField()
    total_fats = serializers.SerializerMethodField()
    current_calories = serializers.SerializerMethodField()
    current_protein = serializers.SerializerMethodField()
    current_carbs = serializers.SerializerMethodField()
    current_fats = serializers.SerializerMethodField()
    
    class Meta:
        model = MealPlan
        fields = ['name', 'days', 'day_meal_completion', 'user_meal_plan', 
                  'total_calories', 'total_protein', 'total_carbs', 'total_fats', 
                  'current_calories', 'current_protein', 'current_carbs', 'current_fats']
        
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
    
    def get_total_calories(self, obj):
        # Summing calories from all meals in the meal plan
        return self.get_nutritional_total(obj, 'calories')

    def get_total_protein(self, obj):
        return self.get_nutritional_total(obj, 'protein')

    def get_total_carbs(self, obj):
        return self.get_nutritional_total(obj, 'carbs')

    def get_total_fats(self, obj):
        return self.get_nutritional_total(obj, 'fats')

    def get_current_calories(self, obj):
        return self.get_current_nutritional_total(obj, 'calories')

    def get_current_protein(self, obj):
        return self.get_current_nutritional_total(obj, 'protein')

    def get_current_carbs(self, obj):
        return self.get_current_nutritional_total(obj, 'carbs')

    def get_current_fats(self, obj):
        return self.get_current_nutritional_total(obj, 'fats')

    def get_nutritional_total(self, obj, nutrient):
        total = Decimal(0)
        day_meal_plans = DayMealPlan.objects.filter(meal_plan=obj.meal_plan)
        for day_meal_plan in day_meal_plans:
            meals = [
                day_meal_plan.breakfast,
                day_meal_plan.mid_morning_snack,
                day_meal_plan.lunch,
                day_meal_plan.afternoon_snack,
                day_meal_plan.dinner,
                day_meal_plan.evening_snack,
            ]
            for meal in meals:
                if meal:
                    total += getattr(meal, nutrient, 0)
        return total
    
    def get_current_nutritional_total(self, obj, nutrient):
        total = Decimal(0)
        # Get only the completed DayMealCompletion records
        completed_meal_completions = DayMealCompletion.objects.filter(
            user_meal_plan=obj,
            completed=True
        )

        # Loop through the completed meals and sum their nutrients
        for completion in completed_meal_completions:
            day_meal_plan = completion.day_meal_plan
            meals = [
                day_meal_plan.breakfast,
                day_meal_plan.mid_morning_snack,
                day_meal_plan.lunch,
                day_meal_plan.afternoon_snack,
                day_meal_plan.dinner,
                day_meal_plan.evening_snack,
            ]
            for meal in meals:
                if meal:
                    total += getattr(meal, nutrient, 0)
        return total
    
class DayMealCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayMealCompletion
        fields = ['completed', ]      
        
    def update(self, instance, validated_data):
        instance.completed = validated_data.get('completed', instance.completed)
        instance.save()
        return instance
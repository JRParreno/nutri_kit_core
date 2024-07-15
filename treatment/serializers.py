from rest_framework import serializers

from food.serializers import FoodSerializers
from .models import Remedy, RemedyFood
from food.models import Food


class RemedyFoodDeficiencySerializers(serializers.ModelSerializer):
    foods = serializers.SerializerMethodField()

    class Meta:
        model = RemedyFood
        fields = ('id', 'foods')
    
    
    def get_foods(self, obj):
        foods = Food.objects.filter(pk=obj.food.pk)
        return FoodSerializers(foods, many=True).data


class RemedyDeficiencySerializers(serializers.ModelSerializer):
    food_remedies = serializers.SerializerMethodField()

    class Meta:
        model = Remedy
        fields = ('id', 'name' ,'description', 'food_remedies')
        
        
        
    def get_food_remedies(self, obj):
        remedies = RemedyFood.objects.filter(remedy=obj)
        return RemedyFoodDeficiencySerializers(remedies, many=True).data

class RemedySerializers(serializers.ModelSerializer):
    class Meta:
        model = Remedy
        fields = '__all__'
        

class RemedyFoodSerializers(serializers.ModelSerializer):
    remedy = RemedySerializers(many=True)
    
    class Meta:
        model = RemedyFood
        fields = '__all__'


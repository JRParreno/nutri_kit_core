from rest_framework import serializers

from food.serializers import FoodSerializers
from .models import Remedy, RemedyFood
from food.models import Food



class RemedySerializers(serializers.ModelSerializer):
    class Meta:
        model = Remedy
        fields = '__all__'
        
class RemedyFoodDeficiencySerializers(serializers.ModelSerializer):
    food = FoodSerializers()
    class Meta:
        model = RemedyFood
        fields = ('id', 'food', 'remedy')
    
        
class RemedyFoodSerializers(serializers.ModelSerializer):
    remedy = RemedySerializers(many=True)
    
    class Meta:
        model = RemedyFood
        fields = '__all__'


class RemedyFoodDetailSerializers(serializers.ModelSerializer):
    food = FoodSerializers()
    class Meta:
        model = RemedyFood
        fields = ('food',)


class RemedyDeficiencySerializers(serializers.ModelSerializer):
    foods = RemedyFoodDetailSerializers(source='remedyfood_set', many=True, read_only=True)
    
    class Meta:
        model = Remedy
        fields = ('id', 'name' ,'description', 'scientific_name','foods')
        
        
        




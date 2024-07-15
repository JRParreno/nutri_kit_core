from rest_framework import serializers
from .models import Food, FoodCategory

class FoodCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = '__all__'

class FoodSerializers(serializers.ModelSerializer):
    # category = FoodCategorySerializers()
    
    class Meta:
        model = Food
        fields = '__all__'
        


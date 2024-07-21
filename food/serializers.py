from rest_framework import serializers
from .models import Food, FoodCategory, Vitamin

class FoodCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = '__all__'



class VitaminSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vitamin
        fields = '__all__'




class FoodSerializers(serializers.ModelSerializer):
    category = FoodCategorySerializers()
    vitamins = VitaminSerializers(many=True)
    
    class Meta:
        model = Food
        fields = '__all__'

        


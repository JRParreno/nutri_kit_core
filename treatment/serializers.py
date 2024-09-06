from rest_framework import serializers

from food.serializers import FoodSerializers
from .models import Remedy, RemedyFood, RemedyFavorite
from food.models import Food



class RemedySerializers(serializers.ModelSerializer):
    class Meta:
        model = Remedy
        fields = '__all__'



class RemedyFavoriteListSerializer(serializers.ModelSerializer):
    remedy = RemedySerializers()
    class Meta:
        model = RemedyFavorite
        fields = ['remedy']
    
    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        super(RemedyFavoriteListSerializer, self).__init__(*args, **kwargs)
    
    def to_representation(self, instance):
        # Return the serialized remedy data directly
        remedy_serializer = self.fields['remedy']
        return remedy_serializer.to_representation(instance.remedy)

class RemedyFoodDeficiencySerializers(serializers.ModelSerializer):
    food = FoodSerializers()
    remedy = RemedySerializers()

    class Meta:
        model = RemedyFood
        fields = ('id', 'food', 'remedy', 'remedy', )


    
        
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
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Remedy
        fields = ('id', 'name' ,'description', 'scientific_name', 'foods', 'is_favorite')
        
        
    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        super(RemedyDeficiencySerializers, self).__init__(*args, **kwargs)
  
    
    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return RemedyFavorite.objects.filter(remedy=obj, user_profile=user.profile).exists()
        return False
    
class RemedyFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemedyFavorite
        fields = ['remedy']
    
    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        super(RemedyFavoriteSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        user_profile = self.context['request'].user.profile
        remedy = validated_data['remedy']
        favorite, created = RemedyFavorite.objects.get_or_create(
            remedy=remedy,
            user_profile=user_profile
        )
        return favorite
from rest_framework import serializers
from .models import Food, FoodCategory, FoodFavorite, Vitamin, VitaminFavorite

class FoodCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = '__all__'



class VitaminSerializers(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Vitamin
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        super(VitaminSerializers, self).__init__(*args, **kwargs)
  
    
    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return VitaminFavorite.objects.filter(vitamin=obj, user_profile=user.profile).exists()
        return False


class FoodSerializers(serializers.ModelSerializer):
    category = FoodCategorySerializers()
    vitamins = VitaminSerializers(many=True)
    is_favorite = serializers.SerializerMethodField()
 
    class Meta:
        model = Food
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        super(FoodSerializers, self).__init__(*args, **kwargs)
  
    
    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return FoodFavorite.objects.filter(food=obj, user_profile=user.profile).exists()
        return False


class FoodFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodFavorite
        fields = ['food']
    
    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        super(FoodFavoriteSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        user_profile = self.context['request'].user.profile
        food = validated_data['food']
        favorite, created = FoodFavorite.objects.get_or_create(
            food=food,
            user_profile=user_profile
        )
        return favorite


class VitaminFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitaminFavorite
        fields = ['vitamin']
    
    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        super(VitaminFavoriteSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        user_profile = self.context['request'].user.profile
        vitamin = validated_data['vitamin']
        favorite, created = VitaminFavorite.objects.get_or_create(
            vitamin=vitamin,
            user_profile=user_profile
        )
        return favorite


class FoodFavoriteListSerializer(serializers.ModelSerializer):
    food = FoodSerializers()
    class Meta:
        model = FoodFavorite
        fields = ['food']
    
    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        super(FoodFavoriteListSerializer, self).__init__(*args, **kwargs)
    
    def to_representation(self, instance):
        # Return the serialized food data directly
        food_serializer = self.fields['food']
        return food_serializer.to_representation(instance.food)


class VitaminFavoriteListSerializer(serializers.ModelSerializer):
    vitamin = VitaminSerializers()
    class Meta:
        model = VitaminFavorite
        fields = ['vitamin']
    
    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        super(VitaminFavoriteListSerializer, self).__init__(*args, **kwargs)
    
    def to_representation(self, instance):
        # Return the serialized vitamin data directly
        vitamin_serializer = self.fields['vitamin']
        return vitamin_serializer.to_representation(instance.vitamin)
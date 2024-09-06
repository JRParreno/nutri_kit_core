from itertools import groupby
from operator import attrgetter
from rest_framework import serializers
from treatment.serializers import RemedySerializers
from .models import Deficiency, DeficiencySymptom, Symptom, DeficiencyFavorite
from treatment.models import Remedy

class SymptomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = '__all__'
        
class DeficiencySymptomSerializers(serializers.ModelSerializer):
    class Meta:
        model = DeficiencySymptom
        fields = '__all__'

        
class DeficiencyDetailSerializers(serializers.ModelSerializer):
    symptoms = SymptomSerializers(many=True)
    remedies = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    class Meta:
        model = Deficiency
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        super(DeficiencyDetailSerializers, self).__init__(*args, **kwargs)

    def get_remedies(self, obj):
        remedies = Remedy.objects.filter(deficiency=obj)
        return RemedySerializers(remedies, many=True).data

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return DeficiencyFavorite.objects.filter(deficiency=obj, user_profile=user.profile).exists()
        return False

class DeficiencySerializers(serializers.ModelSerializer):
    class Meta:
        model = Deficiency
        exclude = ('symptoms',)


class DeficiencyFavoriteListSerializer(serializers.ModelSerializer):
    deficiency = DeficiencySerializers()
    class Meta:
        model = DeficiencyFavorite
        fields = ['deficiency']
    
    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        super(DeficiencyFavoriteListSerializer, self).__init__(*args, **kwargs)
    
    def to_representation(self, instance):
        # Return the serialized deficiency data directly
        deficiency_serializer = self.fields['deficiency']
        return deficiency_serializer.to_representation(instance.deficiency)


class DeficiencyFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeficiencyFavorite
        fields = ['deficiency']
    
    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        super(DeficiencyFavoriteSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        user_profile = self.context['request'].user.profile
        deficiency = validated_data['deficiency']
        favorite, created = DeficiencyFavorite.objects.get_or_create(
            deficiency=deficiency,
            user_profile=user_profile
        )
        return favorite
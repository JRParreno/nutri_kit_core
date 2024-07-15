from rest_framework import serializers
from .models import Deficiency, DeficiencySymptom, Symptom


class SymptomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = '__all__'
        
class DeficiencySymptomSerializers(serializers.ModelSerializer):
    class Meta:
        model = DeficiencySymptom
        fields = '__all__'

class DeficiencySerializers(serializers.ModelSerializer):
    symptoms = SymptomSerializers(many=True)
    
    class Meta:
        model = Deficiency
        fields = '__all__'


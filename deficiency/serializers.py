from rest_framework import serializers
from treatment.serializers import RemedyDeficiencySerializers
from .models import Deficiency, DeficiencySymptom, Symptom
from treatment.models import Remedy, RemedyFood

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
    class Meta:
        model = Deficiency
        fields = '__all__'

    def get_remedies(self, obj):
        remedies = Remedy.objects.filter(deficiency=obj)
        return RemedyDeficiencySerializers(remedies, many=True).data


class DeficiencySerializers(serializers.ModelSerializer):
    class Meta:
        model = Deficiency
        exclude = ('symptoms',)

    
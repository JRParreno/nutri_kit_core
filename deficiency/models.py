from django.db import models

from core.base_models import BaseModel


class Symptom(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class Deficiency(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    symptoms = models.ManyToManyField(Symptom, through='DeficiencySymptom')

        
    class Meta:
        verbose_name = 'Deficiency'
        verbose_name_plural = 'Deficiencies'

    def __str__(self):
        return self.name



class DeficiencySymptom(BaseModel):
    deficiency = models.ForeignKey(Deficiency, on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('deficiency', 'symptom')

    def __str__(self):
        return f"{self.deficiency.name} - {self.symptom.name}"
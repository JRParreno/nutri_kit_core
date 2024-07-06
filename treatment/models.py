from django.db import models

from core.base_models import BaseModel
from deficiency.models import Deficiency
from food.models import Food

class Remedy(BaseModel):
    name = models.CharField(max_length=100)
    deficiency = models.ForeignKey(Deficiency, on_delete=models.CASCADE)
    description = models.TextField()
    
    class Meta:
        verbose_name_plural = 'Remedies'

    def __str__(self):
        return self.name
    

class RemedyFood(BaseModel):
    remedy = models.ForeignKey(Remedy, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('remedy', 'food')

    def __str__(self):
        return f"{self.remedy.name} - {self.food.name}"
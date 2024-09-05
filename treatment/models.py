from django.db import models

from core.base_models import BaseModel
from deficiency.models import Deficiency
from food.models import Food
from user_profile.models import UserProfile

class Remedy(BaseModel):
    name = models.CharField(max_length=100)
    deficiency = models.ForeignKey(Deficiency, on_delete=models.CASCADE)
    description = models.TextField()
    scientific_name =  models.CharField(max_length=100, null=True)
    
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


class RemedyFavorite(BaseModel):
    remedy = models.ForeignKey(Remedy, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('remedy', 'user_profile')

    def __str__(self):
        return f"{self.remedy.name} - {self.user_profile}"
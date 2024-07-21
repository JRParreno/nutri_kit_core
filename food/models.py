from django.db import models
from core.base_models import BaseModel


class FoodCategory(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(
        upload_to='images/food_category/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Food Categories'
    
    def __str__(self):
        return self.name

class Vitamin(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(
        upload_to='images/vitamins/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Food(BaseModel):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    scientificName = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(
        upload_to='images/food/', blank=True, null=True)
    vitamins = models.ManyToManyField(Vitamin, related_name='foods')
    
    
    def __str__(self):
        return self.name + self.scientificName
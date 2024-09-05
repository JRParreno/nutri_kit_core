from django.db import models
from core.base_models import BaseModel
from user_profile.models import UserProfile


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
    scientificName = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(
        upload_to='images/food/', blank=True, null=True)
    vitamins = models.ManyToManyField(Vitamin, related_name='foods')
    
    
    def __str__(self):
        return self.name + self.scientificName


class FoodFavorite(BaseModel):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('food', 'user_profile')

    def __str__(self):
        return f"{self.food} - {self.user_profile}"


class VitaminFavorite(BaseModel):
    vitamin = models.ForeignKey(Vitamin, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('vitamin', 'user_profile')

    def __str__(self):
        return f"{self.vitamin} - {self.user_profile}"
from django.contrib import admin
from .models import Remedy, RemedyFood, RemedyFavorite
from unfold.admin import ModelAdmin
from unfold.contrib.inlines.admin import TabularInline


class RemedyFoodInline(TabularInline):
    model = RemedyFood
    extra = 1  # Number of empty forms to display
    fields = ["food"]

    def get_form_queryset(self, obj):
        """
        Gets all nonrelated objects needed for inlines. Method must be implemented.
        """
        if obj:
            return self.model.objects.filter(remedy=obj)
        return self.model.objects.all()

    def save_new_instance(self, parent, instance, commit=True):
        """
        Extra save method which can for example update inline instances based on current
        main model object. Method must be implemented.
        """
        instance.remedy = parent
        if commit:
            instance.save()
        return instance

@admin.register(Remedy)
class RemedyAdminView(ModelAdmin):
    list_display = ['name', 'deficiency', 'created_at', 'updated_at']
    search_fields = ['name',]
    inlines = [RemedyFoodInline,]


@admin.register(RemedyFood)
class DeficiencySymptomAdminView(ModelAdmin):
    list_display = ['remedy', 'food','created_at', 'updated_at']
    search_fields = ['remedy__name', 'food__name',]


@admin.register(RemedyFavorite)
class RemedyFavoriteAdminView(ModelAdmin):
    list_display = ['remedy', 'user_profile', 'created_at', 'updated_at']
    search_fields = ['remedy__name',]
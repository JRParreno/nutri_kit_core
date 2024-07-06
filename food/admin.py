from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.inlines.admin import NonrelatedTabularInline
from .models import Food, FoodCategory

class FoodCategoryInline(NonrelatedTabularInline):
    model = FoodCategory
    extra = 1  # Number of empty forms to display
    fields = ["name"]

    def get_form_queryset(self, obj):
        """
        Gets all nonrelated objects needed for inlines. Method must be implemented.
        """
        return self.model.objects.all()

    def save_new_instance(self, parent, instance):
        """
        Extra save method which can for example update inline instances based on current
        main model object. Method must be implemented.
        """
        pass

@admin.register(FoodCategory)
class FoodCategoryAdminView(ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name',]


@admin.register(Food)
class FoodAdminView(ModelAdmin):
    list_display = ['name', 'scientificName' ,'category','created_at', 'updated_at']
    search_fields = ['name', 'scientificName',]
    # inlines = [FoodCategoryInline,]
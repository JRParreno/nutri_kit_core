from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.inlines.admin import NonrelatedTabularInline, NonrelatedStackedInline
from .models import Food, FoodCategory, Vitamin

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

class VitaminInline(NonrelatedTabularInline):
    model = Vitamin
    extra = 1  # Number of empty forms to display
    fields = ["name"]

    def get_form_queryset(self, obj):
        """
        Gets all nonrelated objects needed for inlines. Method must be implemented.
        """
        return self.model.objects.all()

    def save_new_instance(self, parent, instance, commit=True):
        """
        Extra save method which can for example update inline instances based on current
        main model object. Method must be implemented.
        """
        instance.question = parent
        if commit:
            instance.save()
        return instance

@admin.register(FoodCategory)
class FoodCategoryAdminView(ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name',]


@admin.register(Vitamin)
class VitaminAdminView(ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name',]

@admin.register(Food)
class FoodAdminView(ModelAdmin):
    list_display = ['name', 'scientificName' ,'category','created_at', 'updated_at']
    search_fields = ['name', 'scientificName',]
    filter_horizontal = ('vitamins',)

from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.inlines.admin import TabularInline
from .models import Food, FoodCategory, Vitamin, FoodFavorite, VitaminFavorite

class FoodCategoryInline(TabularInline):
    model = FoodCategory
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

class VitaminInline(TabularInline):
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


@admin.register(VitaminFavorite)
class VitaminFavoriteAdminView(ModelAdmin):
    list_display = ['vitamin', 'user_profile', 'created_at', 'updated_at']
    search_fields = ['vitamin__name',]

@admin.register(FoodFavorite)
class FoodAdminView(ModelAdmin):
    list_display = ['food', 'user_profile', 'created_at', 'updated_at']
    search_fields = ['food__name',]

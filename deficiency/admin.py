from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.inlines.admin import TabularInline

from deficiency.models import Symptom, Deficiency, DeficiencySymptom

class DeficiencySymptomInline(TabularInline):
    model = DeficiencySymptom
    extra = 1  # Number of empty forms to display
    fields = ["symptom"]

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

@admin.register(Symptom)
class SymptomAdminView(ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name',]
    

@admin.register(Deficiency)
class DeficiencyAdminView(ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name',]
    inlines = [DeficiencySymptomInline,]


@admin.register(DeficiencySymptom)
class DeficiencySymptomAdminView(ModelAdmin):
    list_display = ['symptom', 'deficiency','created_at', 'updated_at']
    search_fields = ['symptom__name', 'deficiency__name',]


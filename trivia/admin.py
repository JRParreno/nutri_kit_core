from django.contrib import admin

from trivia.forms import AnswerForm, CategoryForm, QuestionForm
from .models import  Category, Question, Answer
from unfold.admin import ModelAdmin
from unfold.contrib.inlines.admin import NonrelatedTabularInline

class AnswerInline(NonrelatedTabularInline):
    form = AnswerForm
    model = Answer
    extra = 1  # Number of empty forms to display
    min_num = 1
    max_num = 4
    fields = ["answer_text", "is_correct"]

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
    

@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    search_fields = ['question_text',]
    list_display = ['pk', 'question_text', 'difficulty','created_at', 'updated_at']
    list_filter = ['difficulty',]
    form = QuestionForm
    inlines = [AnswerInline]
    fieldsets = (
        (None, {
            'fields': ('category', 'question_text', 'difficulty'),
            'description': 'Each question must belong to a category and have a difficulty level. '
                           'You can also add multiple possible answers to each question, '
                           'marking one or more as correct.'
        }),
    )
    
    def pk(self, obj):
        return f"{obj.pk}"
    
    pk.short_description = "Question ID"

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    form = CategoryForm

from django import forms
from .models import  Category, Question, Answer
from django.forms.models import BaseInlineFormSet

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        help_texts = {
            'category_name': 'Enter the name of the category.',
            'description': 'Provide a description for the category.',
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        help_texts = {
            'category': 'Select the category for this question.',
            'question_text': 'Enter the text of the question.',
            'difficulty': 'Select the difficulty level of the question.',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = '__all__'
        help_texts = {
            'question': 'Select the question this answer belongs to.',
            'answer_text': 'Enter the text of the answer.',
            'is_correct': 'Check if this is the correct answer.',
        }



class AnswerInlineFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.forms:
            self.forms[0].fields['answer_text'].help_text = "Provide the possible answers for this question. You can add multiple answers, marking one or more as correct."
            for form in self.forms[1:]:
                form.fields['answer_text'].help_text = "Optional: You can add more answers by clicking the 'Add another Answer' button."
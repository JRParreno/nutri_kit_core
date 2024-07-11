from django.db import models

from core.base_models import BaseModel

class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.category_name

class Question(BaseModel):
    EASY = 'Easy'
    MEDIUM = 'Medium'
    HARD = 'Hard'
    DIFFICULTY_LEVELS = [
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question_text = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)

    def __str__(self):
        return self.question_text

class Answer(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text
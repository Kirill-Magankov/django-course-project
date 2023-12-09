from django.contrib import admin
from django.db import models
from django.forms import Textarea

from tester_app.models import Testing, Answer, Question, Result


# Register your models here.

@admin.register(Testing)
class TestingAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 85})}
    }

    list_display = ['name', 'description', 'type', 'slug']
    list_filter = ['type']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 85})}
    }
    list_display = ['test', 'text_question', 'correct_answer']
    list_filter = ['test']
    ordering = ('test', 'text_question')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'result', 'answer', 'is_correct']

    # def get_test(self, obj):
    #     return obj.question.test
    #
    # get_test.short_description = 'test'
    # get_test.admin_order_field = 'question__test'

    # list_filter = ['user', 'question']
    # ordering = ('user',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['test', 'user', 'datetime', 'correct', 'wrong']

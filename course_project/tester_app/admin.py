from django.contrib import admin
from django.db import models
from django.forms import Textarea

from tester_app.models import Testing, Answer, Question, Result, TestSet


# Register your models here.

class QuestionInline(admin.TabularInline):
    model = Question
    fields = ['text_question']

    show_change_link = True
    extra = 0


@admin.register(Testing)
class TestingAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 85})}
    }

    list_display = ['name', 'description', 'type', 'slug']
    list_filter = ['type']
    inlines = [QuestionInline]


class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ['result', 'answer', 'is_correct']
    show_change_link = True
    extra = 0


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['test', 'user', 'datetime', 'correct', 'wrong']
    inlines = [AnswerInline]


class TestSetInline(admin.TabularInline):
    model = TestSet
    fields = ["test_data", "answer"]

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 85})}
    }

    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["test", "text_question"]
    inlines = [TestSetInline]

import datetime
import textwrap

from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from slugify import slugify


# Create your models here.

def slugify_value(value): return slugify(value)


class Testing(models.Model):
    TYPE_CHOICES = (
        ('TEST', 'Тест'),
        ('INTERPRETER', 'Интерпретатор'),
    )

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=150)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='TEST')
    slug = AutoSlugField(populate_from='name', unique=True, slugify=slugify_value)
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('testing', kwargs={'test_slug': self.slug})

    def __str__(self):
        return self.name


class Question(models.Model):
    test = models.ForeignKey(Testing, on_delete=models.CASCADE)
    text_question = models.TextField()
    objects = models.Manager()

    def __str__(self):
        return textwrap.shorten(self.text_question, 60, placeholder="...")  # noqa


class TestSet(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    test_data = models.TextField(blank=True)
    answer = models.TextField()
    objects = models.Manager()

    def __str__(self):
        return f"Correct answer: {self.answer}"


class Result(models.Model):
    test = models.ForeignKey(Testing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=datetime.datetime.now)
    correct = models.IntegerField()
    wrong = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return f'Score: {self.correct} / {self.answer_set.count()}'  # noqa


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    answer = models.TextField()
    is_correct = models.BooleanField(default=False)
    objects = models.Manager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.question.test.type == 'TEST':  # noqa
            self.is_correct = self.answer == str(self.question.testset_set.first().answer)  # noqa
        super().save(force_insert, force_update, using)

    def __str__(self):
        return f"User replied: {self.answer}"
